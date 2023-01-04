import tkinter as tk
from tkinter.messagebox import showinfo


class MainView:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Orienteering_Archieve_Automation")
        self.root.geometry('1000x600')

        self.menu_bar = tk.Menu(self.root, tearoff=0)

    def add_view_to_menu_bar(self, view):

        self.menu_bar.add_command(
            label=view.TAG,
            command=lambda: self.show_target_frame(view)
        )

    def show_target_frame(self, target_frame: tk.Frame):

        for frame in self.root.winfo_children():
            frame.pack_forget()

        target_frame.pack(fill=tk.BOTH, expand=True)

    def prompt_message(self, data: dict[str, str]):

        showinfo(
            title=data['title'],
            message=data['message']
        )

    def start_main_loop(self):

        self.root.config(menu=self.menu_bar)
        self.root.mainloop()
