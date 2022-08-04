#path of the file to be opened
file_path = "ZAM_OpenDRIVETest-1_1-data.xml"

# import functions to read xml file and visualize commonroad objects
import matplotlib.pyplot as plt
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.mp_renderer import MPRenderer

# read in the scenario and planning problem set
scenario, planning_problem_set = CommonRoadFileReader(file_path).open()

#time step for simulation
n = 50

# plot the planning problem and the scenario
plt.ion()
plt.figure(figsize=(25, 10))
for t in range(0, n):
    rnd = MPRenderer()
    scenario.draw(rnd, draw_params={'time_begin': t})
    planning_problem_set.draw(rnd)
    rnd.render()
    plt.pause(0.5)
    plt.clf()