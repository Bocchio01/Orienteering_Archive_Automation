from enum import IntEnum
from ocad import ocad


class OCADFilter(IntEnum):
    BOUNDBOX = 29
    COORDSYSTEM = 1039
    MAPNOTES = 1061


def get_query(ocdFile: str, filter: int):
    query = ocad._get_ocad_strings(
        ocdFile,
        output_typ="dict",
        filter=filter
    )

    if isinstance(query, dict):
        return query.get(filter, [])
    elif isinstance(query, list):
        return query[filter] if filter < len(query) else []


def getCoordSystem(ocdFile: str) -> None | dict:
    coordinate_system = get_query(
        ocdFile=ocdFile,
        filter=OCADFilter.COORDSYSTEM.value
    )

    if len(coordinate_system) > 0:
        coordinate_system = coordinate_system[0].split("\t")
        coordinate_system_dict = dict(
            (x[0], x[1:])
            for x in coordinate_system[1:]
        )
        return coordinate_system_dict
    else:
        print(
            f"File '{ocdFile}' doesn't have any coordinate system associated")


def getBoundBox(ocdFile: str) -> None | dict:
    export_boundaries = get_query(
        ocdFile=ocdFile,
        filter=OCADFilter.BOUNDBOX.value
    )

    if len(export_boundaries) > 0:
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
        print(
            f"File '{ocdFile}' doesn't have any default export boundaries associated")


def getMapNotes(ocdFile: str) -> None | str:
    map_notes = get_query(
        ocdFile=ocdFile,
        filter=OCADFilter.MAPNOTES.value
    )

    if len(map_notes) > 0:
        map_notes = map_notes[0].replace("\r\n", "<br />")
        return map_notes
    else:
        print(f"File '{ocdFile}' doesn't have any map notes associated")
