import tkinter as tk
from tkinter import ttk

from Utils.TypingHint.settings import GUIType


class TwoFrameView(tk.Frame):
    def __init__(self, master: tk.Tk, opt: GUIType):

        tk.Frame.__init__(
            self,
            master=master,
            **opt['main_frame']
        )

        self.left_frame = tk.Frame(
            self,
            bg=opt['bg_general']
        )

        self.hr = ttk.Separator(self, orient=tk.VERTICAL)

        self.right_frame = tk.Frame(
            self,
            bg=opt['bg_general']
        )

        self.grid_columnconfigure(0, weight=1, minsize=300, )
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=10, minsize=300)
        self.grid_rowconfigure(0, weight=1, minsize=300)
        self.left_frame.grid(row=0, column=0, sticky='NSEW')
        self.hr.grid(row=0, column=1, sticky='NS', padx=10)
        self.right_frame.grid(row=0, column=2, sticky='NSEW')
