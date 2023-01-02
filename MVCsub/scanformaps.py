import os
import tkinter as tk
from MVCmain.ABC import ABCController
from tkinter.filedialog import askdirectory


class ScanForMapsController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_root = main_controller.view.root

        self.view = ScanForMapsView(
            master=self.main_root,
            opt=self.main_controller.get_gui_opt()
        )
        self.model = ScanForMapsModel(controller=self)

        self.view.scan_button.config(command=self.scan_for_maps)
        self.view.save_button.config(command=self.save_maps)

    def scan_for_maps(self):
        # open file dialog and get path

        dirs = []
        title = 'Choose Directory'
        while True:
            dir = askdirectory(title=title)
            if not dir:
                break
            dirs.append(dir)

        folder_list = self.model.get_maps_path()
        self.view.text.insert(tk.END, '\n'.join(folder_list))

    def save_maps(self):
        self.main_controller.model.save_json(
            self.model.get_maps_path(), 'assets/maps.json')


class ScanForMapsView(tk.Frame):
    def __init__(self, master, opt: dict):

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )

        self.text = tk.Text(self, **opt['text_config'])
        self.scan_button = tk.Button(self, text="Scan", **opt['button_config'])
        self.save_button = tk.Button(self, text="Save", **opt['button_config'])

        self.scan_button.pack()
        self.save_button.pack()
        self.text.pack()


class ScanForMapsModel:
    def __init__(self, controller):
        self.controller = controller

    def get_maps_path(self):
        MEGA = self.controller.main_controller.get_mega_settings()
        os.sep = '/'

        base_file_path = MEGA['path']
        folders_to_exclude = MEGA['folders_to_exclude']

        folders_list = [
            os.sep.join([base_file_path, folder])
            for folder in os.listdir(base_file_path)
            if (
                os.path.isdir(os.sep.join([base_file_path, folder])) and
                folder not in folders_to_exclude
            )
        ]

        return folders_list
