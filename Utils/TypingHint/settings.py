import enum
from typing import Literal, TypedDict
from tkinter.font import Font


class BorderType(TypedDict):
    borderwidth: int
    relief: str


class VisualizerType(TypedDict):
    bg: str
    bd: int
    relief: str
    height: int
    width: int


class FontType(TypedDict):
    family: str
    size: int
    weight: Literal['normal'] | Literal['bold']


class TextConfigType(TypedDict):
    bg: str
    font: Font


class ComboboxType(TypedDict):
    state: str
    font: Font


class MainFrameType(TypedDict):
    bg: str
    borderwidth: int
    relief: Literal['solid']


class GUIType(TypedDict):
    bg_general: str
    bg_button: str
    bg_visualizer: str
    dim_visualizer: int
    border: BorderType
    visualizer_config: VisualizerType
    font: FontType

    text_font: Font
    text_config: TextConfigType
    button_config: TextConfigType
    combobox_config: ComboboxType
    main_frame: MainFrameType

    title_config: TextConfigType
    subtitle_config: TextConfigType
