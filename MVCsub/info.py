import tkinter as tk
from PIL import ImageTk, Image
from MVCmain.ABC import ABCController


class InfoController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_root = main_controller.view.root

        self.view = InfoView(
            master=self.main_root,
            opt=self.main_controller.get_gui_opt()
        )
        self.model = InfoModel(controller=self)


class InfoView(tk.Frame):
    def __init__(self, master: tk.Tk, opt: dict):

        logo = ImageTk.PhotoImage(
            Image.open(fr'assets/img/ori.png'),
            size=(100, 100)
        )

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )

        self.logo = tk.Label(
            self,
            image=logo,
            bg=opt['bg_general']
        )
        self.logo.image = logo

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

    def get_hello_world(self):
        return "Hello World!"
