from enum import IntEnum
import os
from typing import Sized
from ocad import ocad
import utm


class OCADFilter(IntEnum):
    BOUNDBOX = 29
    COORDSYSTEM = 1039
    MAPNOTES = 1061


def get_query(ocd_file: str, filter: int) -> list | dict | None:

    if not os.path.isfile(ocd_file):
        print(f"File {ocd_file} not found")
        raise FileNotFoundError

    query = ocad._get_ocad_strings(
        ocd_file,
        output_typ="dict",
        filter=filter
    )

    if isinstance(query, dict):
        return query.get(filter, [])
    elif isinstance(query, list):
        return query[filter] if filter < len(query) else []


def getCoordSystem(imp_file: str) -> dict | None:
    coordinate_system = get_query(
        ocd_file=imp_file,
        filter=OCADFilter.COORDSYSTEM.value
    )

    if isinstance(coordinate_system, Sized) and len(coordinate_system) > 0:
        coordinate_system = coordinate_system[0].split("\t")
        coordinate_system_dict = dict(
            (x[0], x[1:])
            for x in coordinate_system[1:]
        )
        return coordinate_system_dict
    else:
        return None


def getBoundBox(imp_file: str) -> dict | None:
    export_boundaries = get_query(
        ocd_file=imp_file,
        filter=OCADFilter.BOUNDBOX.value
    )

    if isinstance(export_boundaries, Sized) and len(export_boundaries) > 0:
        export_boundaries = export_boundaries[0].split("\t")

        # We divide by factor 25600 because of Ocad Unit. The result is a paper coordinate
        export_boundaries_dict = {
            "name": export_boundaries[0],
            **dict(
                (x[0], int(x[1:]) / 25600)
                for x in export_boundaries[1:]
            )
        }
        return export_boundaries_dict
    else:
        return None


def getMapNotes(map_file: str) -> str | None:
    map_notes = get_query(
        ocd_file=map_file,
        filter=OCADFilter.MAPNOTES.value
    )

    if isinstance(map_notes, Sized) and len(map_notes) > 0:
        map_notes = map_notes[0].replace("\r\n", "<br />")
        return map_notes
    else:
        return None


def getGeoCoords(ocd_files_path: dict[str, str]):
    # Why do I need to relay on the boundBox... I want the center of gravity of the map?
    coordSystem = getCoordSystem(ocd_files_path['map_file'])
    boundBox = getBoundBox(ocd_files_path['imp_file'])

    if not coordSystem or not boundBox:
        return None

    center_x = int(coordSystem['x'])
    center_y = int(coordSystem['y'])
    scale = int(float(coordSystem['m']))

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

    coord = [sum(x)/2 for x in zip(NW, SE)]
    geographic_coordinates = {
        'lat': coord[0],
        'lon': coord[1]
    }

    return geographic_coordinates


def getMapDict(ocd_files_path: dict[str, str]) -> dict:

    coords_system = getCoordSystem(ocd_files_path['map_file'])
    export_boundaries = getBoundBox(ocd_files_path['imp_file'])
    geographic_coordinates = getGeoCoords(ocd_files_path)
    notes = getMapNotes(ocd_files_path['map_file'])

    mapDict = {

        'scale': "{:.0f}".format(float(coords_system['m'])) if coords_system else "No scale found",
        'grivation': "{:.2f}".format(float(coords_system['a'])) if coords_system else "No grivation found",
        'export_boundaries': export_boundaries if export_boundaries else "No export boundaries found",
        'notes': notes.replace("<br />", "\r\n") if notes else "No map notes found",
        'geographic_coordinates': geographic_coordinates if geographic_coordinates else "No geographic coordinates found"
    }

    return mapDict
