import json
from tkinter import font

from MVCmain.observable import Observable
from Utils.TypingHint.settings import GUIType
from Utils.variable import DEBUG


class Model:

    def __init__(self):
        self.settings = Observable({})
        self.settings.addCallback(self.save_json)

        self.gui_opt = Observable({})

        self.map_data = Observable()
        self.map_ID_selected = Observable('')

    def get_settings(self) -> dict:

        if not self.settings.get():
            file = self.read_json(r"assets/settings.json")
            self.settings.set({**file})

        return self.settings.get()

    def get_gui_opt(self) -> GUIType:

        if not self.gui_opt.get():
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
            opt['title_config'] = {
                'bg': opt['bg_general'],
                'font': font.Font(**opt['font_title'])
            }
            opt['subtitle_config'] = {
                'bg': opt['bg_general'],
                'font': font.Font(**opt['font_subtitle'])
            }

            if DEBUG:
                for el in opt:
                    if isinstance(opt[el], dict):
                        opt[el] = {
                            **opt[el],
                            'borderwidth': 2,
                            'relief': 'solid'
                        }

            self.gui_opt.set(opt)

        return self.gui_opt.get()

    @staticmethod
    def save_json(data, path=r"assets/settings.json", mode='w'):
        with open(path, mode) as outfile:
            json.dump(
                data,
                outfile,
                sort_keys=False,
                indent=4
            )

    @staticmethod
    def read_json(path=r"assets/settings.json"):
        file = open(path)
        content = json.load(file)
        file.close()
        return content
