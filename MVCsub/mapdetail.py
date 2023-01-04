from email.mime import image
import tkinter as tk

from MVCmain.ABC import ABCController
from Utils.TypingHint.settings import GUIType
from PIL import ImageTk, Image


class MapDetailController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = MapDetailView(
            master=self.main_view.root,
            opt=self.main_model.get_gui_opt()
        )
        self.model = MapDetailModel(controller=self)

        self.main_model.map_ID_selected.addMultipleCallback([
            lambda e: self.view.text_label.config(
                text='Selezionato ' + self.main_model.map_ID_selected.get()
            ),
            lambda e: self.main_view.show_target_frame(self.view)
        ]
        )


class MapDetailView(tk.Frame):
    TAG = 'Map Detail'

    def __init__(self, master: tk.Tk, opt: GUIType):

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )

        image = Image.open(
            fr'C:\Users\Bocchio\Dropbox\Applicazioni\BocchioDevApp\MapsGif\Liceo Giovio 1000.gif')
        image.thumbnail((500, 500))
        image = ImageTk.PhotoImage(image)

        self.image_label = tk.Label(self, image=image)
        self.image_label.image = image  # type: ignore

        self.text = 'This is some info that goes on the left side of the screen'
        self.text_label = tk.Label(self, text=self.text)

        self.image_label.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.text_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


class MapDetailModel:
    def __init__(self, controller):
        self.controller = controller
