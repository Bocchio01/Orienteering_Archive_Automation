import datetime
import os
import tkinter as tk
from tkinter import ttk
import glob

from MVCmain.ABC import ABCController
from Utils.multiframetemplate import TwoFrameView
from Utils.observable import Observable
from Utils.TypingHint.settings import GUIType
import Utils.ocadinterface as OCAD

from Utils.variable import *


class FoldersAnalysisController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = FoldersAnalysisView(
            master=self.main_view.root,
            opt=self.main_model.get_gui_opt()
        )
        self.model = FoldersAnalysisModel(controller=self)

        self.model.map_data.addMultipleCallback([
            lambda e: self.view.update_list(self.model.map_data.get()),
        ])

        self.view.refresh.config(
            command=self.model.scan
        )

        self.view.tree.bind(
            '<Double-Button-1>',
            self.item_selected
        )
        self.view.entry.bind(
            '<KeyRelease>',
            lambda e: self.view.search_by_map_name(
                self.view.entry.get('1.0', 'end-1c'))
        )

    def item_selected(self, event):
        for selected_item in self.view.tree.selection():
            item = self.view.tree.item(selected_item)
            self.main_model.map_ID_selected.set(item['values'][0])

        self.model.scan()


class FoldersAnalysisView(TwoFrameView):
    TAG = 'Folder Analysis'

    def __init__(self, master: tk.Tk, opt: GUIType):

        TwoFrameView.__init__(self, master=master, opt=opt)

        self.entry = tk.Text(self.left_frame, height=3, width=10)
        self.refresh = tk.Button(
            self.left_frame, text='Refrech', **opt['button_config'])

        self.tree = ttk.Treeview(self.right_frame, show='headings')
        self.scrollbar = ttk.Scrollbar(
            self.right_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )

        columns = ('Map_Name', 'is_folder_ok')
        self.tree["columns"] = columns

        self.tree.heading(columns[0], text=columns[0])
        self.tree.heading(columns[1], text=columns[1])

        self.tree.configure(yscroll=self.scrollbar.set)

        self.entry.pack()
        self.refresh.pack()

        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def update_list(self, map_datas: list[str]) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        for map_data in map_datas:
            self.tree.insert('', tk.END, values=(
                map_data['mapID'],
                map_data['is_folder_ok'],
            ))

    def search_by_map_name(self, query: str):
        selections = []

        for child in self.tree.get_children():
            if query.lower() in self.tree.item(child)['values'][0].lower():
                selections.append(child)

        self.tree.selection_set(selections)


class FoldersAnalysisModel:
    def __init__(self, controller):
        self.controller = controller
        self.map_data = Observable()

    def scan(self, base_path: str = BASE_FILE_PATH, folders_to_exculde: list[str] = FOLDERS_TO_EXCLUDE):
        folders_list = self.get_folders_list(
            base_path=base_path,
            folders_to_exculde=folders_to_exculde
        )
        complete_folder_status = self.get_folders_status(folders=folders_list)
        self.get_OCD_main_data(folder_status=complete_folder_status)

    def get_folders_list(self, base_path: str = BASE_FILE_PATH, folders_to_exculde: list[str] = FOLDERS_TO_EXCLUDE) -> list[str]:
        """
        Get the list of the folder inside the base_path folder.

        :param str base_path: Parent folder to be searched, defaults to BASE_FILE_PATH
        :param list[str] folders_to_exculde: Any folders that will be ignored by the search, defaults to FOLDERS_TO_EXCLUDE
        :return list[str]: List of string containing the name of the folders inside the parent. Folders name starting with '_' are ignored by default (supposed to be still under-work)
        """

        folders_list = [
            folder
            for folder in os.listdir(base_path)
            if os.path.isdir(os.sep.join([base_path, folder]))
            and not any(i in folder for i in folders_to_exculde)
            and not folder.startswith('_')
        ]

        # self.folders_list = folders_list

        return folders_list

    def get_folders_status(self, folders: list[str] = []) -> list:

        folders_OCD_status = map(
            lambda folder: self.get_OCD_file_in_folder(
                folder_to_be_looked=folder
            ),
            folders
        )

        # Any other check over the folder about file-containing, mapData.json...

        complete_folder_status = list(zip(
            folders,
            list(folders_OCD_status)
            # list(folders_FILE_status)
            # ...
        ))

        # print(complete_folder_status[0])

        return complete_folder_status

    def get_OCD_file_in_folder(self, folder_to_be_looked: str) -> dict[str, bool | str]:
        complete_folder = os.path.join(
            BASE_FILE_PATH,
            folder_to_be_looked,
            folder_to_be_looked
        )

        map_file = False
        imp_file = False
        is_folder_ok = False

        match(len(glob.glob(complete_folder + ' *.ocd'))):
            # if .ocd hasn't been added yet
            case 0:
                map_file = False
                imp_file = False
                is_folder_ok = True

            case 1 | 2:
                map_file = glob.glob(complete_folder + ' *[0-9].ocd')
                imp_file = glob.glob(
                    complete_folder + ' *[0-9] impaginazione.ocd')

                map_file = map_file[0] if len(map_file) == 1 else False
                imp_file = imp_file[0] if len(imp_file) == 1 else False

                is_folder_ok = bool(map_file and imp_file)

            case _:
                is_folder_ok = False

        folder_status = {
            'mapFile': map_file,
            'impFile': imp_file,
            'is_folder_ok': is_folder_ok
        }

        return folder_status

    def get_OCD_main_data(self, folder_status: list) -> list:
        outjson = list()

        for folder_name, folders_OCD_status in folder_status:
            map_file_related_data = {}
            imp_file_related_data = {}

            if folders_OCD_status['mapFile']:
                map_file_related_data = {
                    'lastMod': datetime.datetime.fromtimestamp(os.path.getmtime(folders_OCD_status['mapFile'])).__str__(),
                    # 'expFile': folders_OCD_status['mapFile'].split('.')[0] + '.gif',
                    'mapNotes': OCAD.getMapNotes(folders_OCD_status['mapFile']),
                    'coordSystem': OCAD.getCoordSystem(folders_OCD_status['mapFile']),
                }

            if folders_OCD_status['impFile']:
                imp_file_related_data = {
                    'boundBox': OCAD.getBoundBox(folders_OCD_status['impFile']),
                }

            outjson.append({
                'mapID': folder_name,
                **map_file_related_data,
                **imp_file_related_data,
                **folders_OCD_status
            })

        # print(outjson[0])
        self.map_data.set(outjson)
        return outjson
