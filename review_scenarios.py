import os
import matplotlib.pyplot as plt
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.mp_renderer import MPRenderer


# load the CommonRoad scenario that has been created in the CommonRoad tutorial
file_path = '/home/micrl/code/commonroad_tutorial/commonroad-search/scenarios/tutorial/USA_Peach-2_1_T-1.xml'

scenario, planning_problem_set = CommonRoadFileReader(file_path).open()


plt.ion()
plt.figure(figsize=(25, 10))
# plot the scenario for each time step
for i in range(0, 40):
    rnd = MPRenderer()
    scenario.draw(rnd, draw_params={'time_begin': i})
    planning_problem_set.draw(rnd)
    rnd.render()
    plt.pause(0.5)
    plt.clf()