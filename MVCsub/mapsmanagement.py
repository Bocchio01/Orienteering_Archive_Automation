import glob
import os
import subprocess
import tkinter as tk

from PIL import Image, ImageTk
import requests
from Utils.Interfaces.database import AltevistaDB

import Utils.Interfaces.ocad as OCAD
from MVCmain.ABC import ABCController
from Utils.GUIWidgets.customwidgets import DashBoardHCView, MultiFrameView, TreeView
from Utils.observable import Observable
from Utils.variable import *
from Utils.Interfaces.xml import generateXML
import json


class MapsManagementController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = MapsManagementView(
            master=self.main_view.root,
        )
        self.model = self.main_model.register_module(MapsManagementModel())

        # self.DB = AltevistaDB(API_URL=API_URL)

        self.model.files_paths.addMultipleCallback([
            lambda e: self.view.maps.update_tree(
                list(e.keys())
            ),
        ])

        self.view.refresh_data.config(
            command=self.model.scan_path
        )

        # self.view.db_maps.tree.bind(
        #     '<Button1-ButtonRelease>',
        #     self.db_map_selected
        # )

        self.view.maps.tree.bind(
            '<Button1-ButtonRelease>',
            self.map_selected
        )

        self.view.add_map_to_db.config(
            command=self.add_map_to_db
        )

        # self.view.update_map_to_db.config(
        #     command=self.update_map_to_db
        # )

        self.view.generate_xml.config(
            command=self.generate_xml
        )

        self.model.scan_path()

    def generate_xml(self):
        map_data = []

        for map in self.view.maps.get_selected_row():
            map_data.append(self.model.get_map_data(map))

        export_file = generateXML(map_data)

        # program_path = r"C:/Program Files (x86)/OCAD/OCAD 12/OCAD 12 Mapping Solution_32bit.exe"
        # subprocess.run([program_path, export_file])

    def map_selected(self, event):

        selected_row = self.view.maps.get_selected_row()

        if len(selected_row) == 1:
            map_data = self.model.get_map_data(selected_row[0])
            self.view.dashboard.update_entries(map_data)
            self.view.update_image(map_data['gif_file'])

        else:
            self.view.dashboard.update_entries({})

    def add_map_to_db(self):
        map_data = self.view.dashboard.get_entries()
        # AltevistaDB(API_URL=API_URL).add_map(map_data)

        response = requests.post(
            url=API_URL,
            data=json.dumps({
                'action': 'AddMap',
                'data': map_data
            })
        )

        print(response.text)

    # def update_map_to_db(self):
    #     entries = self.view.dashboard.get_entries()
    #     self.DB.edit_map(entries)


class MapsManagementView(MultiFrameView):
    TAG = 'Maps Management'

    def __init__(self, master: tk.Tk):

        MultiFrameView.__init__(self, master=master, weights=(1, 5, 1))

        self.maps = TreeView(
            master=self.frames[0],
            **{
                'columns': ('Map_Name'),
                'show': 'headings'
            }
        )

        self.refresh_data = tk.Button(
            self.frames[0],
            text='Update Maps Data'
        )

        self.dashboard = DashBoardHCView(
            master=self.frames[1],
        )

        self.add_map_to_db = tk.Button(
            self.frames[1],
            text='Add Map to DB'
        )

        # self.update_map_to_db = tk.Button(
        #     self.frames[1],
        #     text='Update Map to DB'
        # )

        self.generate_xml = tk.Button(
            self.frames[1],
            text='Generate XML'
        )

        self.image_label = tk.Label(self.frames[2])

        # self.pdf_viewver = pdf. ShowPdf().pdf_view(
        #     self.frames[2],
        #     # pdf_location=r"location",
        #     width=50,
        #     height=100
        # )

        self.maps.pack(fill=tk.BOTH, expand=True)
        self.refresh_data.pack(fill=tk.X, padx=10, pady=10)

        self.dashboard.columnconfigure(0, weight=1, minsize=100)
        self.dashboard.columnconfigure(1, weight=5, minsize=100)
        self.dashboard.pack(fill=tk.BOTH, expand=True)
        self.add_map_to_db.pack(fill=tk.X, padx=10, pady=10)
        # self.update_map_to_db.pack(fill=tk.X, padx=10, pady=10)
        self.generate_xml.pack(fill=tk.X, padx=10, pady=10)

        self.image_label.pack(fill=tk.BOTH, expand=True)
        # self.pdf_viewver.pack(fill=tk.BOTH, expand=True)

    def update_image(self, image_path: str):
        if not image_path:
            image_path = fr'assets/img/ori.png'
            return

        image = Image.open(image_path)
        image.thumbnail((650, 650))
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image  # type: ignore

        # self.pdf_viewver = pdf.ShowPdf().pdf_view(
        #     self.frames[2],
        #     pdf_location=r'C:/Users/Bocchio/Documents/MEGAsync/Orienteering/Carte/Cernobbio/Cernobbio 2500.pdf',
        #     width=50,
        #     height=100
        # )

        # self.pdf_viewver.pack(fill=tk.BOTH, expand=True)


class MapsManagementModel:
    def __init__(self):
        self.files_paths = Observable()
        # self.DB_maps_data = Observable()

    # def merge_data(self):
    #     maps: dict[str, dict[str, str]] | None = self.files_paths.get()
    #     DB_maps: dict[str, dict[str, str]] | None = self.DB_maps_data.get()

    #     if maps is not None and DB_maps is not None:
    #         copies = []

    #         for map_name, map_data in maps.items():
    #             if map_name in DB_maps:
    #                 DB_maps[map_name].update(map_data)
    #                 copies.append(map_name)

    #         maps = {k: v for k, v in maps.items()
    #                 if k not in copies}
    #         self.files_paths.set(maps)
    #         self.DB_maps_data.set(DB_maps)

    def scan_path(self, base_path: str = BASE_FILE_PATH, folders_to_exculde: list[str] = FOLDERS_TO_EXCLUDE) -> dict[str, dict[str, str]]:
        """
        Scan the base_path folder and return a dictionary containing the path of the files inside the folder.

        :param str base_path: Parent folder to be searched, defaults to BASE_FILE_PATH
        :param list[str] folders_to_exculde: Any folders that will be ignored by the search, defaults to FOLDERS_TO_EXCLUDE
        :return dict[str, dict[str, str]]: Dictionary containing the path of the files inside the folder.
        """

        folders_paths = self.get_folders_list(
            base_path=base_path,
            folders_to_exculde=folders_to_exculde
        )
        files_paths = self.get_files_paths(folders=folders_paths)
        self.files_paths.set(files_paths)

        return files_paths

    def get_folders_list(self, base_path: str = BASE_FILE_PATH, folders_to_exculde: list[str] = FOLDERS_TO_EXCLUDE) -> list[str]:
        """
        Get the list of the folder inside the base_path folder.

        :param str base_path: Parent folder to be searched, defaults to BASE_FILE_PATH
        :param list[str] folders_to_exculde: Any folders that will be ignored by the search, defaults to FOLDERS_TO_EXCLUDE
        :return list[str]: List of string containing the name of the folders inside the parent. Folders name starting with '_' are ignored by default (supposed to be still under-work)
        """

        folders_list = [
            os.sep.join([base_path, folder])
            for folder in os.listdir(base_path)
            if os.path.isdir(os.sep.join([base_path, folder]))
            and not any(i in folder for i in folders_to_exculde)
            and not folder.startswith('_')
        ]

        return folders_list

    def get_files_paths(self, folders: list[str] = []) -> dict[str, dict[str, str]]:
        """
        Search for all the possible files of interest inside the given folders.
        The files of interest are:
            - Map file (OCD)
            - Impagination file (OCD)
            - Exported impagination file (GIF)
            - Exported impagination file (PDF)

        :param list[str] folders: List of folder to be checked, defaults to []
        :return dict[str, dict[str, str]]: Dict containing the path of the files of interest for each folder
        """

        files_paths = {}

        for folder in folders:
            map_name = os.path.basename(folder)
            ocd_location = os.path.join(folder, map_name)
            exp_location = os.path.join(folder, 'Export', map_name)

            map_file = glob.glob(f'{ocd_location} *[0-9].ocd')
            imp_file = glob.glob(f'{ocd_location} *[0-9] impaginazione.ocd')
            pdf_file = glob.glob(f'{exp_location}.pdf')
            gif_file = glob.glob(f'{exp_location}.gif')

            files_paths[map_name] = {
                'map_name': map_name,
                'map_file': map_file[0] if len(map_file) == 1 else False,
                'imp_file': imp_file[0] if len(imp_file) == 1 else False,
                'pdf_file': pdf_file[0] if len(pdf_file) == 1 else False,
                'gif_file': gif_file[0] if len(gif_file) == 1 else False
            }

        return files_paths

    def get_map_data(self, map_name: str) -> dict[str, str]:
        """
        Get the data of the given map_name from the DB.

        :param str map_name: Name of the map to be searched
        :return dict[str, str]: Dictionary
        """

        map_files_paths = self.files_paths.get()[map_name]
        map_data = {
            'name': map_name,
            **OCAD.getMapDict(map_files_paths),
            **map_files_paths
        }

        # print(map_data)

        return map_data
