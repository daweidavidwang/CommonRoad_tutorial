#path of the file to be opened
file_path = "converted_from_OpenDRIVETest.xml"

# import functions to read xml file and visualize commonroad objects
import matplotlib.pyplot as plt
from commonroad.common.file_reader import CommonRoadFileReader
from commonroad.visualization.mp_renderer import MPRenderer

# read in the scenario and planning problem set
scenario, planning_problem_set = CommonRoadFileReader(file_path).open()

# plot the planning problem and the scenario

plt.figure(figsize=(25, 10))

rnd = MPRenderer()
scenario.draw(rnd, draw_params={'time_begin': 1})
planning_problem_set.draw(rnd)
rnd.render()
plt.show()
