import tkinter as tk
from PIL import ImageTk, Image
from MVCmain.ABC import ABCController
from Utils.TypingHint.settings import GUIType


class InfoController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = InfoView(
            master=self.main_view.root,
            opt=self.main_model.get_gui_opt()
        )
        self.model = InfoModel(controller=self)


class InfoView(tk.Frame):
    def __init__(self, master: tk.Tk, opt: GUIType):

        image = Image.open(fr'assets/img/ori.png')
        image.thumbnail((300, 300))
        image = ImageTk.PhotoImage(image)

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )

        self.logo = tk.Label(
            self,
            image=image,
            bg=opt['bg_general']
        )
        self.logo.image = image  # type: ignore

        self.presentation = tk.Label(
            self,
            text="Orienteering Archive Automation",
            **opt['text_config']
        )

        self.logo.pack()
        self.presentation.pack()


class InfoModel:
    def __init__(self, controller):
        self.controller = controller
