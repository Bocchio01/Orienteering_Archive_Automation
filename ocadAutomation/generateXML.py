import os
import xml.etree.ElementTree as ET
import json


# Element.set(‘attrname’, ‘value’) – Modifying element attributes.
# Element.SubElement(parent, new_childtag) -creates a new child tag under the parent.
# Element.write(‘filename.xml’)-creates the tree of xml into another file.
# Element.pop() -delete a particular attribute.
# Element.remove() -to delete a complete tag.

file = open('./ocadAutomation/OcadFileList.json')
file_list = json.load(file)
file.close()

# output_dir = r"C:\Users\Bocchio\Documents\MEGAsync\Orienteering\Carte\_Script XML\ocadAutomation\generated\\"


for file_path in file_list:

    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    dir_name = os.path.dirname(file_path)
    dir_name = dir_name.replace('/', '\\')

    data_file = open(os.sep.join([dir_name, 'API', 'mapData.json']))
    data = json.load(data_file)['mapDatas']
    data_file.close()

    # print(data)

    # fileScale = [int(x) for x in file_name.split(' ') if x.isnumeric()][0]
    if (data['boundBox']):
        OcadScript = ET.Element("OcadScript")
        fileOpen = ET.SubElement(OcadScript, "File.Open")
        ET.SubElement(fileOpen, "File").text = os.sep.join(
            [dir_name, file_name + ' impaginazione' + file_extension])

        # PDF export
        treePDF = ET.parse('./ocadAutomation/template/ExportPDF.xml')
        rootPDF = treePDF.getroot()

        rootPDF.find('File').text = os.sep.join(
            [dir_name, 'API', file_name + ".pdf"])
        PARTOFMAP = rootPDF.find('PartOfMap')
        PARTOFMAP.find('L').text = str(
            data['boundBox']['l']).replace('.', ',')
        PARTOFMAP.find('R').text = str(
            data['boundBox']['r']).replace('.', ',')
        PARTOFMAP.find('B').text = str(
            data['boundBox']['b']).replace('.', ',')
        PARTOFMAP.find('T').text = str(
            data['boundBox']['t']).replace('.', ',')
        rootPDF.find('ExportScale').text = str(data['coordSystem']['m'])

        # GIF export
        treeGIF = ET.parse('./ocadAutomation/template/ExportGIF.xml')
        rootGIF = treeGIF.getroot()

        rootGIF.find('File').text = os.sep.join(
            # [dir_name, 'API', file_name + ".gif"]
            ['C:/Users/Bocchio/Dropbox/Applicazioni/BocchioDevApp/MapsGif',
                file_name + ".gif"]
        )
        PARTOFMAP = rootGIF.find('PartOfMap')
        PARTOFMAP.find('L').text = str(
            data['boundBox']['l']).replace('.', ',')
        PARTOFMAP.find('R').text = str(
            data['boundBox']['r']).replace('.', ',')
        PARTOFMAP.find('B').text = str(
            data['boundBox']['b']).replace('.', ',')
        PARTOFMAP.find('T').text = str(
            data['boundBox']['t']).replace('.', ',')

        # Append filled template to OcadScript node
        OcadScript.append(rootPDF)
        OcadScript.append(rootGIF)

        fileClose = ET.SubElement(OcadScript, "File.Close")
        ET.SubElement(fileClose, "Enabled").text = 'true'

        tree = ET.ElementTree(OcadScript)
        tree.write(os.sep.join([dir_name, 'API', 'Export.xml']))
    else:
        print("File {} senza coordinate per l'esportazione".format(file_name))
