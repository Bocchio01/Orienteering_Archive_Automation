import json
import os
import xml.etree.ElementTree as ET

from Utils.variable import BASE_FILE_PATH

OUTPUT_PATH = BASE_FILE_PATH + os.sep + "Export.xml"


def generateXML(map_data: list[dict[str, str]]) -> str:

    print(json.dumps(map_data, indent=4, sort_keys=True))

    OcadScript = ET.Element("OcadScript")

    for map in map_data:

        map['bound'] = {
            key: str(coord).replace('.', ',')
            for key, coord in map['export_boundaries'].items()
        }

        fileOpen = ET.SubElement(OcadScript, "File.Open")
        ET.SubElement(fileOpen, "File").text = map['imp_file']

        # Append filled template to OcadScript node
        exp_location = os.path.join(os.path.dirname(
            map['imp_file']), 'Export', map['name'])

        if not os.path.exists(os.path.dirname(exp_location)):
            os.makedirs(os.path.dirname(exp_location))

        OcadScript.append(PDF_format(
            export_path=f"{exp_location}.pdf",
            data=map
        ))
        OcadScript.append(GIF_format(
            export_path=f"{exp_location}.gif",
            data=map
        ))

        fileClose = ET.SubElement(OcadScript, "File.Close")
        ET.SubElement(fileClose, "Enabled").text = 'true'

        tree = ET.ElementTree(OcadScript)
        tree.write(OUTPUT_PATH)

    return OUTPUT_PATH


def PDF_format(export_path, data):
    tree = ET.parse('./assets/xml/ExportPDF.xml')
    root = tree.getroot()

    root.find('File').text = export_path
    PARTOFMAP = root.find('PartOfMap')
    PARTOFMAP.find('L').text = data['bound']['l']
    PARTOFMAP.find('R').text = data['bound']['r']
    PARTOFMAP.find('B').text = data['bound']['b']
    PARTOFMAP.find('T').text = data['bound']['t']
    root.find('ExportScale').text = str(data['scale'])

    return root


def GIF_format(export_path, data):
    tree = ET.parse('./assets/xml/ExportGIF.xml')
    root = tree.getroot()

    root.find('File').text = export_path
    PARTOFMAP = root.find('PartOfMap')
    PARTOFMAP.find('L').text = data['bound']['l']
    PARTOFMAP.find('R').text = data['bound']['r']
    PARTOFMAP.find('B').text = data['bound']['b']
    PARTOFMAP.find('T').text = data['bound']['t']

    return root
