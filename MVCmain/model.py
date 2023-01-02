import json
import logging
from tkinter import font

from MVCmain.observable import Observable
from Utils._TypingHint.settings import GUIType


class Model:

    def __init__(self):
        logging.debug(f"Model")
        self.settings = Observable({})
        self.settings.addCallback(self.save_json)

        self.gui_opt = Observable({})

    def get_settings(self) -> dict:

        if not self.settings.get():
            logging.debug(f"Model")
            file = self.read_json(r"assets/settings.json")
            self.settings.set({**file})

            logging.debug(f"Model:settings:{self.settings.get()}")

        return self.settings.get()

    def get_gui_opt(self) -> GUIType:

        if not self.gui_opt.get():
            logging.debug(f"Model")
            opt = {**self.get_settings()['GUI']}
            opt['text_font'] = font.Font(**opt['font'])
            opt['text_config'] = {
                'bg': opt['bg_general'],
                'font': opt['text_font']
            }
            opt['button_config'] = {
                'bg': opt['bg_button'],
                'font': opt['text_font']
            }
            opt['combobox_config'] = {
                'state': 'readonly',
                'font': opt['text_font']
            }
            opt['visualizer_config'] = {
                'bg': opt['bg_visualizer'],
                'bd': 1,
                'relief': 'solid',
                'height': opt['dim_visualizer'],
                'width': opt['dim_visualizer']
            }
            opt['main_frame'] = {
                'bg': opt['bg_general'],
                'borderwidth': 2,
                'relief': 'solid'
            }

            self.gui_opt.set(opt)

        return self.gui_opt.get()

    @staticmethod
    def save_json(data, path=r"assets/settings.json", mode='w'):
        logging.debug(f"Model:path:{path}")
        with open(path, mode) as outfile:
            json.dump(
                data,
                outfile,
                sort_keys=False,
                indent=4
            )

    @staticmethod
    def read_json(path=r"assets/settings.json"):
        logging.debug(f"Model:path:{path}")
        file = open(path)
        content = json.load(file)
        file.close()
        return content
