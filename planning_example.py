import sys, os
sys.path.append(os.getcwd()+"/commonroad-search")

import matplotlib.pyplot as plt
from commonroad.visualization.mp_renderer import MPRenderer


from commonroad.common.file_reader import CommonRoadFileReader
from SMP.maneuver_automaton.maneuver_automaton import ManeuverAutomaton
from SMP.motion_planner.motion_planner import MotionPlanner
from SMP.motion_planner.utility import MotionPrimitiveStatus, initial_visualization, update_visualization, plot_state

scenario = 'commonroad-search/scenarios/tutorial/ZAM_Tutorial_Urban-3_2.xml'
motionprimitives = 'V_9.0_9.0_Vstep_0_SA_-0.2_0.2_SAstep_0.4_T_0.5_Model_BMW320i.xml'

# load scenario and planning problem set, retrieve the first planning problem
scenario, planning_problem_set = CommonRoadFileReader(scenario).open()
planning_problem = list(planning_problem_set.planning_problem_dict.values())[0]

# create maneuver automaton
automaton = ManeuverAutomaton.generate_automaton(motionprimitives)

# create and execute planner
planner = MotionPlanner.AStarSearch(scenario=scenario,
									planning_problem=planning_problem,
									automaton=automaton)
path_solution, _, _ = planner.execute_search()

traj = []
for primitive in path_solution:
    for state in primitive:
        traj.extend([state])


n = 35

# plot the planning problem and the scenario
plt.ion()
plt.figure(figsize=(25, 10))
for t in range(0, n):
    rnd = MPRenderer()
    scenario.draw(rnd, draw_params={'time_begin': t})
    planning_problem_set.draw(rnd)
    traj[t].draw(rnd)
    rnd.render()
    plt.pause(0.5)
    plt.clf()