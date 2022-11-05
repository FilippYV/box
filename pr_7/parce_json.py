import ast
import json


def parse_json():
    with open("data.json", "r") as file:
        data = file.read().replace("[", "").replace("]", "").split(",\n")
        for data_list in data:
            result = json.loads(data_list)
            print("Time: " + result['co_two_level'])
            print("\ttemperature: " + result['temperature'])
            print("\tsound: " + result["sound"])
            print("\tconcentrationCO2: " + result['illuminance'])
            print("\tconcentrationVOC: " + result['sound'])

