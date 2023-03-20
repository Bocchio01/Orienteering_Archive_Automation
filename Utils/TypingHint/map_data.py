import enum
from typing import Literal, TypedDict
from tkinter.font import Font


class boundBox(TypedDict):
    b: int
    l: int
    r: int
    t: int
    name: str


class coordSystem(TypedDict):
    a: int
    b: int
    c: int
    d: int
    g: int
    i: int
    m: int
    r: int
    x: int
    y: int


class generalInfo(TypedDict):
    expFile: str
    impFile: str
    mapFile: str
    mapID: int
    mapName: str
    mapNotes: str


class leaflet(TypedDict):
    center: list[float]
    grivation: float


class mapDatas(TypedDict):
    boundBox: boundBox
    coordSystem: coordSystem
    generalInfo: generalInfo
    leaflet: leaflet


class mapJson(TypedDict):
    mapID: str
    dateTime: str
    mapDatas: mapDatas


class file_path(TypedDict):
    map_name: str
    map_file: str
    imp_file: str
    pdf_file: str
    gif_file: str


class files_paths(TypedDict):
    map_name: file_path
