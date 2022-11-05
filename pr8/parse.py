import json
import xml.etree.ElementTree as ET

tree = ET.parse('test.xml')
root = tree.getroot()

for sub_item in root:
    for item in sub_item:
        print(item.tag, "/", item.text)

with open("../static/data.json", "r") as file_json:
    dictData = json.load(file_json)
    print(json.dumps(dictData, indent=4))