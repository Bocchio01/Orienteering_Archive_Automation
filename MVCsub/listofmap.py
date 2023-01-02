import datetime
import os
import tkinter as tk
from tkinter import ttk
import glob

from MVCmain.ABC import ABCController
from Utils.observable import Observable
from Utils._TypingHint.settings import GUIType
import Utils.ocadinterface as OCAD


class ListOfMapController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_root = main_controller.view.root
        self.main_model = main_controller.model

        self.view = ListOfMapView(
            master=self.main_root,
            opt=self.main_model.get_gui_opt()
        )
        self.model = ListOfMapModel(controller=self)

        self.model.map_data.addMultipleCallback([
            lambda e: self.view.update_list(self.model.map_data.get()),
        ])

        self.view.refresh.config(
            command=self.model.update_data
        )


class ListOfMapView(tk.Frame):
    def __init__(self, master: tk.Tk, opt: GUIType):

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )

        self.entry = tk.Text(self, height=3)
        self.refresh = tk.Button(self, text='Refrech', **opt['button_config'])

        self.tree = ttk.Treeview(self, show='headings')
        scrollbar = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.tree.yview)

        columns = ('Map_Name', 'Date_Last_Mod', 'Scale')
        self.tree["columns"] = columns

        self.tree.heading(columns[0], text=columns[0])
        self.tree.heading(columns[1], text=columns[1])
        self.tree.heading(columns[2], text=columns[2])

        self.tree.configure(yscroll=scrollbar.set)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.entry.grid(row=0, column=0)
        self.refresh.grid(row=0, column=1)
        self.tree.grid(row=1, column=0, sticky='nesw')
        scrollbar.grid(row=1, column=1, sticky='ns')

        self.entry.bind(
            '<KeyRelease>',
            lambda e: self.search_by_map_name(self.entry.get('1.0', 'end-1c'))
        )
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def update_list(self, map_datas: list[str]) -> None:
        for row in self.tree.get_children():
            self.tree.delete(row)

        for map_data in map_datas:
            self.tree.insert('', tk.END, values=(
                map_data['generalInfo']['mapName'],
                map_data['generalInfo']['lastMod'],
                map_data['coordSystem']['m']
            ))

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            # show a message
            # showinfo(title='Information', message=','.join(record))

    def search_by_map_name(self, query: str):
        selections = []

        for child in self.tree.get_children():
            if query.lower() in self.tree.item(child)['values'][0].lower():
                selections.append(child)

        self.tree.selection_set(selections)


BASE_FILE_PATH = r"C:\Users\Bocchio\Documents\MEGAsync\Orienteering\Carte"
FOLDERS_TO_EXCLUDE = [
    '_Luigi',
    '_protected',
    'API'
]


class ListOfMapModel:
    def __init__(self, controller):
        self.controller = controller
        self.folders_list = Observable()
        self.map_data = Observable()
        self.update_data()

    def update_data(self) -> None:
        folder_list = self.get_list_of_folder()
        map_paths = self.get_list_of_map(folder_list=folder_list)
        self.get_map_data(map_paths=map_paths)

    def get_list_of_folder(self) -> list[str]:

        folders_list = [
            os.sep.join([BASE_FILE_PATH, folder])
            for folder in os.listdir(BASE_FILE_PATH)
            if os.path.isdir(os.sep.join([BASE_FILE_PATH, folder]))
            and not any(i in folder for i in FOLDERS_TO_EXCLUDE)
            and not folder.startswith('_')
            and len(glob.glob(os.path.join(BASE_FILE_PATH, folder, folder + '*.ocd'))) > 0
        ]

        self.folders_list.set(folders_list)

        return folders_list

    def get_list_of_map(self, folder_list: list[str]) -> dict:
        map_paths = {}
        for folder in folder_list:
            ocadFiles = glob.glob(os.path.join(folder, '*.ocd'))
            if len(ocadFiles) <= 2:
                map_paths[folder] = {
                    'folder': folder,
                    'mapFile': [i for i in ocadFiles if 'impaginazione' not in i][0],
                    'impFile': [i for i in ocadFiles if 'impaginazione' in i][0]
                }
            else:
                print(f"Più file rilevati nella cartella {folder}")

        return map_paths

    def get_map_data(self, map_paths: dict) -> list:
        outjson = list()

        for index, (key, map_path) in enumerate(map_paths.items()):
            outjson.append({
                'generalInfo': {
                    'mapID': index,
                    'lastMod': datetime.datetime.fromtimestamp(os.path.getmtime(map_path['mapFile'])).__str__(),
                    'mapName': map_path['folder'].split(os.sep)[-1],
                    'mapFile': map_path['mapFile'].split(os.sep)[-1] if type(map_path['mapFile']) is str else None,
                    'impFile': map_path['impFile'].split(os.sep)[-1] if type(map_path['impFile']) is str else None,
                    'expFile': map_path['mapFile'].split('.')[0] + '.gif' if type(map_path['mapFile']) is str else None,
                    'mapNotes': OCAD.getMapNotes(map_path['mapFile']) if type(map_path['mapFile']) is str else None
                },
                'coordSystem': OCAD.getCoordSystem(map_path['mapFile']) if type(map_path['mapFile']) is str else None,
                'boundBox': OCAD.getBoundBox(map_path['impFile']) if type(map_path['impFile']) is str else None,
            })

        print(outjson[0])
        self.map_data.set(outjson)
        return outjson
