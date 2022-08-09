
class TIConstraints:
    a_min = -8
    a_max = 15
    s_min = 0
    s_max = 150
    v_min = 0
    v_max = 35
    j_min = -30
    j_max = 30
import os
import matplotlib.pyplot as plt
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.mp_renderer import MPRenderer
from commonroad.geometry.shape import Rectangle
from commonroad.scenario.obstacle import DynamicObstacle, ObstacleType
from commonroad.scenario.trajectory import Trajectory,State
from commonroad.prediction.prediction import TrajectoryPrediction
from vehiclemodels import parameters_vehicle3
import pkg_resources
import numpy as npy
pkg_resources.require("scipy>=1.1.0")
pkg_resources.require("cvxpy>=1.0.0")
from cvxpy import *
def plot_state_vector(x : Variable, c : TIConstraints, s_obj = None):
    plt.figure(figsize=(10,10))
    N = x.shape[1]-1
    s_max = npy.maximum(150,100+0*npy.ceil(npy.amax((x.value)[0,:].flatten())*1.1/10)*10)

    # Plot (x_t)_1.
    plt.subplot(4,1,1)
    x1 = (x.value)[0,:].flatten()
    plt.plot(npy.array(range(N+1)),x1,'g')
    if s_obj is not None:
        plt.plot(npy.array(range(1,N+1)),s_obj[0],'b')
        plt.plot(npy.array(range(1,N+1)),s_obj[1],'r')
    plt.ylabel(r"$s$", fontsize=16)
    plt.yticks(npy.linspace(c.s_min, s_max, 3))
    plt.ylim([c.s_min, s_max])
    plt.xticks([])

    # Plot (x_t)_2.
    plt.subplot(4,1,2)
    x2 = (x.value)[1,:].flatten()
    plt.plot(npy.array(range(N+1)),x2,'g')
    plt.yticks(npy.linspace(c.v_min,c.v_max,3))
    plt.ylim([c.v_min, c.v_max+2])
    plt.ylabel(r"$v$", fontsize=16)
    plt.xticks([])

    # Plot (x_t)_3.
    plt.subplot(4,1,3)
    x2 = (x.value)[2,:].flatten()
    plt.plot(npy.array(range(N+1)),x2,'g')
    plt.yticks(npy.linspace(c.a_min,c.a_max,3))
    plt.ylim([c.a_min, c.a_max+2])
    plt.ylabel(r"$a$", fontsize=16)
    plt.xticks([])

    # Plot (x_t)_4.
    plt.subplot(4,1,4)
    x2 = (x.value)[3,:].flatten()
    plt.plot(npy.array(range(N+1)), x2,'g')
    plt.yticks(npy.linspace(c.j_min,c.j_max,3))
    plt.ylim([c.j_min-1, c.j_max+1])
    plt.ylabel(r"$j$", fontsize=16)
    plt.xticks(npy.arange(0,N+1,5))
    plt.xlabel(r"$k$", fontsize=16)
    plt.tight_layout()
    plt.show()

# load the CommonRoad scenario that has been created in the CommonRoad tutorial
file_path = 'ZAM_Tutorial-1_2_T-1.xml'

scenario, planning_problem_set = CommonRoadFileReader(file_path).open()


# plt.ion()
# plt.figure(figsize=(25, 10))
# # plot the scenario for each time step
# for i in range(0, 40):
#     rnd = MPRenderer()
#     scenario.draw(rnd, draw_params={'time_begin': i})
#     planning_problem_set.draw(rnd)
#     rnd.render()
#     plt.pause(0.5)
#     plt.clf()

# problem data
N  = 40  # number of time steps
n  = 4   # length of state vector 
m  = 1   # length of input vector
dT = scenario.dt # time step


# set up variables
x = Variable(shape=(n,N+1)) # optimization vector x contains n states per time step 
u = Variable(shape=(N)) # optimization vector u contains 1 state

# set up constraints
c = TIConstraints()
c.a_min = -6 # Minimum feasible acceleration of vehicle
c.a_max = 6 # Maximum feasible acceleration of vehicle
c.s_min = 0 # Minimum allowed position
c.s_max = 100 # Maximum allowed position
c.v_min = 0 # Minimum allowed velocity (no driving backwards!)
c.v_max = 35 # Maximum allowed velocity (speed limit)
c.j_min = -15 # Minimum allowed jerk 
c.j_max = 15 # Maximum allowed jerk

# weights for cost function
w_s = 0
w_v = 8
w_a = 2
w_j = 2
Q = npy.eye(n)*npy.transpose(npy.array([w_s,w_v,w_a,w_j]))
w_u = 1
R = w_u

## Vehicle model
A = npy.array([[1,dT,(dT**2)/2,(dT**3)/6],
               [0,1,dT,(dT**2)/2],
               [0,0,1,dT],
               [0,0,0,1]])
B = npy.array([(dT**4)/24,
               (dT**3)/6,
               (dT**2)/2,
               dT]).reshape([n,])

# get the initial state of the ego vehicle from the planning problem set
planning_problem = list(planning_problem_set.planning_problem_dict.values())[0]
initial_state = planning_problem.initial_state

# extract obstacle from scenario
dyn_obstacles = scenario.dynamic_obstacles

# create constraints for minimum and maximum position
s_min = [] # minimum position constraint
s_max = [] # maximum position constraint

# initial state of vehicle for the optimization problem (longitudinal position, velocity, acceleration, jerk)
x_0 = npy.array([initial_state.position[0],
                 initial_state.velocity,
                 0.0,
                 0.0]).reshape([n,]) # initial state

# go through obstacle list and distinguish between following and leading vehicle
for o in dyn_obstacles:
    if o.initial_state.position[0] < x_0[0]:
        print('Following vehicle id={}'.format(o.obstacle_id))
        prediction = o.prediction.trajectory.state_list
        for p in prediction:
            s_min.append(p.position[0]+o.obstacle_shape.length/2.+2.5)
    else:
        print('Leading vehicle id={}'.format(o.obstacle_id))
        prediction = o.prediction.trajectory.state_list
        for p in prediction:
            s_max.append(p.position[0]-o.obstacle_shape.length/2.-2.5)

# plot vehicle motions
plt.plot(range(1,len(s_min)+1),s_min,'b')
plt.plot(range(1,len(s_max)+1),s_max,'r')

# reference velocity
v_ref = 30.0
# Set up optimization problem
states = []
cost = 0
# initial state constraint
constr = [x[:,0] == x_0]

tiConstraints = [x[1,:] <= c.v_max, x[1,:] >= c.v_min] # velocity
tiConstraints += [x[2,:] <= c.a_max, x[2,:] >= c.a_min] # acceleration
tiConstraints += [x[3,:] <= c.j_max, x[3,:] >= c.j_min] # jerk

for k in range(N):
    # cost function
    cost += quad_form(x[:,k+1] - npy.array([0,v_ref,0,0],), Q)\
           + R * u[k] ** 2
    # time variant state and input constraints
    constr.append(x[:,k+1] == A @ x[:,k] + B * u[k])

    # add obstacle constraint
    ## sometimes s_max and s_min is empty, check validation first
    if len(s_max)>0:
        constr.append(x[0,k+1] <= s_max[k]) 
    if len(s_max)>0:
        constr.append(x[0,k+1] >= s_min[k]) 

# sums problem objectives and concatenates constraints.
# create optimization problem
prob = Problem(Minimize(cost), constr + tiConstraints)

# Solve optimization problem
prob.solve(verbose=True)
print("Problem is convex: ",prob.is_dcp())
print("Problem solution is "+prob.status)

# plot results
plot_state_vector(x, TIConstraints())

# plot results
# plot_state_vector(x, c, [s_min, s_max])

x_result = x.value
s_ego = x_result[0,:].flatten()
v_ego = x_result[1,:].flatten()

# generate state list of the ego vehicle's trajectory
state_list = [initial_state]
for i in range(1, N):
    orientation = initial_state.orientation
    # compute new position
    # add new state to state_list    
    state_list.append(State(**{'position': npy.array([s_ego[i],0]), 'orientation': orientation,
                               'time_step': i, 'velocity': v_ego[i]*npy.cos(orientation),
                               'velocity_y': v_ego[i]*npy.sin(orientation)}))

# create the planned trajectory starting at time step 1
ego_vehicle_trajectory = Trajectory(initial_time_step=1, state_list=state_list[1:])
# create the prediction using the planned trajectory and the shape of the ego vehicle

vehicle3 = parameters_vehicle3.parameters_vehicle3()
ego_vehicle_shape = Rectangle(length=vehicle3.l, width=vehicle3.w)
ego_vehicle_prediction = TrajectoryPrediction(trajectory=ego_vehicle_trajectory,
                                              shape=ego_vehicle_shape)

# the ego vehicle can be visualized by converting it into a DynamicObstacle
ego_vehicle_type = ObstacleType.CAR
ego_vehicle = DynamicObstacle(obstacle_id=100, obstacle_type=ego_vehicle_type,
                              obstacle_shape=ego_vehicle_shape, initial_state=initial_state,
                              prediction=ego_vehicle_prediction)


plt.ion()
plt.figure(figsize=(25, 10))
# plot the scenario and the ego vehicle for each time step
for i in range(0, 40):
    rnd = MPRenderer()
    scenario.draw(rnd, draw_params={'time_begin': i})
    ego_vehicle.draw(rnd, draw_params={'time_begin': i, 'dynamic_obstacle': {
        'vehicle_shape': {'occupancy': {'shape': {'rectangle': {
            'facecolor': 'g'}}}}}})
    planning_problem_set.draw(rnd)
    rnd.render()
    plt.pause(0.5)
    plt.clf()