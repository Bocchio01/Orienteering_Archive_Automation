from ocad import ocad
import generateXMLScript
import json
import os


file = open('./ocadAutomation/OcadFileList.json')
file_list = json.load(file)


for file_path in file_list:

    file_name, file_extension = os.path.splitext(os.path.basename(file_path))
    dir_name = os.path.dirname(file_path)

    try:
        coordinate_system_dict = {}
        coordinate_system_str = ocad._get_ocad_strings(
            os.sep.join([dir_name, file_name + file_extension]), output_typ="dict", filter=1039).get(1039)[0]
        coordinate_system_list = coordinate_system_str.split("\t")
        coordinate_system_dict = dict((x[0], x[1:])
                                      for x in coordinate_system_list[1:])

    except:
        print("File '{}' doesn't have any coordinate system associated".format(
            file_name))
        pass

    try:
        export_boundaries_dict = {}
        export_boundaries_str = ocad._get_ocad_strings(
            os.sep.join([dir_name, file_name + ' impaginazione' + file_extension]), output_typ="dict", filter=29).get(29)[0]
        export_boundaries_list = export_boundaries_str.split("\t")
        export_boundaries_dict = {
            "name": export_boundaries_list[0], **dict((x[0], int(x[1:]) / 25600) for x in export_boundaries_list[1:])}  # We divide by factor 25600 because of Ocad Unit. The result is a paper coordinate

    except:
        print("File '{}' doesn't have any default export boundaries associated".format(
            file_name))
        pass

    try:
        map_notes = {}
        map_notes = ocad._get_ocad_strings(
            os.sep.join([dir_name, file_name + file_extension]), output_typ="dict", filter=1061).get(1061)[0]
    except:
        print("File '{}' doesn't have any map notes associated".format(
            file_name))
        pass

    finale_dict = {
        "coordinateSystem": coordinate_system_dict,
        "exportPaperCoordinates": export_boundaries_dict,
        "mapNotes": map_notes}

    with open(os.sep.join([dir_name, 'API', 'mapData.json']), "w") as outfile:
        json.dump(finale_dict, outfile, sort_keys=True, indent=4)
