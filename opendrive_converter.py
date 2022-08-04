input_path = "data.xodr"  # replace empty string
output_path = "."
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

