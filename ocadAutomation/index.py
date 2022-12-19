import json
import os
from datetime import datetime
from ocad import ocad
import utm
# import numpy as np


# Retrive all mapData.json file and organize information in a singular file (.json)
# Use this generated file as a sort of database to call in order to retrieve info about maps

def formatJson(outfile, index=None):
    global outjson
    return json.dump(
        {
            'dateTime': str(datetime.now()),
            'mapDatas': outjson[index] if index is not None else outjson,
        },
        outfile,
        sort_keys=True,
        indent=4
    )


def dumpJSON(folder):
    global outjson, index

    if not os.path.exists(os.sep.join([folder, 'API'])):
        os.makedirs(os.sep.join([folder, 'API']))

    with open(os.sep.join([folder, 'API', 'mapData.json']), "w") as outfile:
        formatJson(outfile, index)


def getCoordSystem(ocdFile):
    try:
        coordinate_system_str = ocad._get_ocad_strings(
            ocdFile,
            output_typ="dict",
            filter=1039
        ).get(1039)[0]
        coordinate_system_list = coordinate_system_str.split("\t")
        coordinate_system_dict = dict(
            (x[0], x[1:])
            for x in coordinate_system_list[1:]
        )
        return coordinate_system_dict
    except:
        print("File '{}' doesn't have any coordinate system associated".format(ocdFile))


def getBoundBox(ocdFile):
    try:
        export_boundaries_str = ocad._get_ocad_strings(
            ocdFile,
            output_typ="dict",
            filter=29
        ).get(29)[0]
        export_boundaries_list = export_boundaries_str.split("\t")

        # We divide by factor 25600 because of Ocad Unit. The result is a paper coordinate
        export_boundaries_dict = {
            "name": export_boundaries_list[0],
            **dict(
                (x[0], int(x[1:]) / 25600)
                for x in export_boundaries_list[1:]
            )
        }
        return export_boundaries_dict
    except:
        print("File '{}' doesn't have any default export boundaries associated".format(
            ocdFile))


def getMapNotes(ocdFile):
    try:
        map_notes = ocad._get_ocad_strings(
            ocdFile,
            output_typ="dict",
            filter=1061
        ).get(1061)[0]
        return map_notes.replace("\r\n", "<br \>")
    except:
        print("File '{}' doesn't have any map notes associated".format(ocdFile))


def getLeafletData(mapDict):
    coordSystem = mapDict['coordSystem']
    boundBox = mapDict['boundBox']

    center_x = int(coordSystem['x'])
    center_y = int(coordSystem['y'])
    scale = int(float(coordSystem['m']))
    grivation = float(coordSystem['a'])

    # bound = [l t; r b] .* (mapScale / 1000);

    NW = utm.to_latlon(
        center_x + boundBox['l'] * scale / 1000,
        center_y + boundBox['t'] * scale / 1000,
        32,
        northern=True
    )

    SE = utm.to_latlon(
        center_x + boundBox['r'] * scale / 1000,
        center_y + boundBox['b'] * scale / 1000,
        32,
        northern=True
    )

    leaflet = {
        'grivation': grivation,
        'center': [sum(x)/2 for x in zip(NW, SE)]
    }

    return leaflet


base_file_path = r"C:\Users\Bocchio\Documents\MEGAsync\Orienteering\Carte"
folders_list = [
    i for i in os.listdir(base_file_path)
    if os.path.isdir(os.sep.join([base_file_path, i]))
]

# print(*[file.replace(base_file_path, '') for file in file_name_list], sep='\n')
folders_to_exclude = [
    '_Luigi',
    '_QGIS',
    '_Simbologia',
    '_protected',
    'API'
]

folders_target = [
    os.sep.join([base_file_path, folder])
    for folder in folders_list
    if not any(i in folder for i in folders_to_exclude)
]
outjson = list()

for index, folder in enumerate(folders_target):

    print(index, folder)
    name_folder = os.path.basename(os.path.normpath(folder))
    outjson.insert(index, {})

    file_list = os.listdir(folder)
    # print('File list:', *file_list, sep='\n', end='\n\n')

    ocd_file = [
        file for file in file_list
        if '.ocd' in str(file)
    ]
    # print('Ocad files:', *ocd_file, sep='\n', end='\n\n')

    # Check for multiple src file of the map. Only one per folder allowed.
    mapFile = [i for i in ocd_file if 'impaginazione' not in i]

    match len(mapFile):
        case 0:
            print(
                'Nessun file mappa trovato all\'interno della cartella "{}". Controllare.'.format(folder))
        case 1:
            mapFile = mapFile[0]
            # print('File mappa trovato all\'interno della cartella "{}".'.format(folder))
        case _:
            print(
                'Multipli file mappa trovati all\'interno della cartella "{}".'.format(folder))

    # Check for multiple impagination file of the map. Only one per folder allowed.
    impFile = [i for i in ocd_file if 'impaginazione' in i]

    match len(impFile):
        case 0:
            print(
                'Nessun file impaginazione trovato all\'interno della cartella "{}". Controllare.'.format(folder))
        case 1:
            impFile = impFile[0]
            # print('File impaginazione trovato all\'interno della cartella "{}".'.format(folder))
        case _:
            print(
                'Multipli file impaginazione trovati all\'interno della cartella "{}".'.format(folder))

    outjson[index] = {
        **outjson[index],
        'generalInfo': {
            'mapID': index,
            'mapName': name_folder,
            'mapFile': mapFile if type(mapFile) is str else None,
            'impFile': impFile if type(impFile) is str else None,
            'expFile': mapFile.split('.')[0] + '.gif' if type(mapFile) is str else None,
            'mapNotes': getMapNotes(os.sep.join([folder, mapFile])) if type(mapFile) is str else None
        },
        'coordSystem': getCoordSystem(os.sep.join([folder, mapFile])) if type(mapFile) is str else None,
        'boundBox': getBoundBox(os.sep.join([folder, impFile])) if type(impFile) is str else None,
    }

    if outjson[index]['coordSystem'] and outjson[index]['boundBox']:

        outjson[index] = {
            **outjson[index],
            'leaflet': getLeafletData(outjson[index])
        }

    dumpJSON(folder)


with open(os.sep.join([base_file_path, 'mapData.json']), "w") as outfile:
    formatJson(outfile)

with open(os.sep.join([r'C:/Users/Bocchio/Dropbox/Applicazioni/BocchioDevApp', 'mapData.json']), "w") as outfile:
    formatJson(outfile)
