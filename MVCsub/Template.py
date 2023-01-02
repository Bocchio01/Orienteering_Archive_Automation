import tkinter as tk

from MVCmain.ABC import ABCController
from Utils.TypingHint.settings import GUIType


class TemplateController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = TemplateView(
            master=self.main_view.root,
            opt=self.main_model.get_gui_opt()
        )
        self.model = TemplateModel(controller=self)


class TemplateView(tk.Frame):
    def __init__(self, master: tk.Tk, opt: GUIType):

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )


class TemplateModel:
    def __init__(self, controller):
        self.controller = controller
