import tkinter as tk

from MVCmain.ABC import ABCController


class TemplateController:
    def __init__(self, main_controller: ABCController):
        self.main_controller = main_controller
        self.main_view = main_controller.view
        self.main_model = main_controller.model

        self.view = TemplateView(master=self.main_view.root)
        self.model = self.main_model.register_module(TemplateModel())


class TemplateView(tk.Frame):
    def __init__(self, master: tk.Tk):

        tk.Frame.__init__(
            self,
            master=master
        )


class TemplateModel:
    def __init__(self):
        pass
