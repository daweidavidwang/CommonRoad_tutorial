input_path = "Your OpenDRIVE file to convert"  # replace empty string
output_path = "DESTINATION DIR"
# General Imports
import os
from lxml import etree

from commonroad.scenario.scenario import Tag
from commonroad.common.file_writer import CommonRoadFileWriter, OverwriteExistingFile
from commonroad.planning.planning_problem import PlanningProblemSet
from commonroad.common.file_reader import CommonRoadFileReader
from crdesigner.map_conversion.map_conversion_interface import opendrive_to_commonroad

# load OpenDRIVE file, parse it, and convert it to a CommonRoad scenario
scenario = opendrive_to_commonroad(input_path)

# store converted file as CommonRoad scenario
writer = CommonRoadFileWriter(
    scenario=scenario,
    planning_problem_set=PlanningProblemSet(),
    author="Sebastian Maierhofer",
    affiliation="Technical University of Munich",
    source="CommonRoad Scenario Designer",
    tags={Tag.URBAN},
)
writer.write_to_file(output_path+ "/" + "converted_from_OpenDRIVETest.xml",
                     OverwriteExistingFile.ALWAYS)

from crdesigner.map_conversion.opendrive.opendrive_parser.parser import parse_opendrive
from crdesigner.map_conversion.opendrive.opendrive_conversion.network import Network

# OpenDRIVE parser to load file
with open("{}".format(input_path), "r") as file_in:
    opendrive = parse_opendrive(etree.parse(file_in).getroot())

# create OpenDRIVE intermediate network object
road_network = Network()

# convert OpenDRIVE file
road_network.load_opendrive(opendrive)

# export to CommonRoad scenario
scenario = road_network.export_commonroad_scenario()

# store converted file as CommonRoad scenario
writer = CommonRoadFileWriter(
    scenario=scenario,
    planning_problem_set=PlanningProblemSet(),
    author="Sebastian Maierhofer",
    affiliation="Technical University of Munich",
    source="CommonRoad Scenario Designer",
    tags={Tag.URBAN},
)
writer.write_to_file(os.path.dirname(os.path.realpath(__file__)) + "/" + "ZAM_OpenDRIVETest-1_1-T1.xml",
                     OverwriteExistingFile.ALWAYS)