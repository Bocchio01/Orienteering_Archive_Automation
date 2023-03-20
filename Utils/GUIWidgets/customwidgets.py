import tkinter as tk
from tkinter import ttk


class MultiFrameView(ttk.Frame):
    def __init__(self, master: tk.Tk, weights: tuple = (1, 10)):

        ttk.Frame.__init__(
            self,
            master=master,
            style='Main.TFrame',
            border=2,
            relief=tk.SOLID,
            padding=10
        )

        self.frames = []

        for index, weight in enumerate(weights, start=0):
            self.frames.append(tk.Frame(self))
            self.frames[index].grid(row=0, column=2*index, sticky='NSEW')
            self.grid_columnconfigure(2*index, weight=weight)

            if index < len(weights) - 1:
                ttk.Separator(self, orient=tk.VERTICAL).grid(
                    row=0, column=2*index+1, sticky='NS', padx=10
                )
                self.grid_columnconfigure(2*index+1, weight=0)

        self.grid_rowconfigure(0, weight=1)


class TreeView(tk.Frame):
    def __init__(self, master: tk.Tk | tk.Frame, **karws):

        tk.Frame.__init__(
            self,
            master=master,
        )

        self.query_box = tk.Text(
            self,
            height=1,
            width=15
        )

        self.tree = ttk.Treeview(
            self,
            show='headings'
        )

        if karws.get('scrollbar'):
            self.scrollbar = ttk.Scrollbar(
                self,
                orient='vertical',
                command=self.tree.yview
            )

            self.tree.configure(yscrollcommand=self.scrollbar.set)

        if karws.get('columns'):

            columns: str | list[str] = karws.get('columns')

            self.tree.configure(columns=columns)
            if isinstance(columns, str):
                self.tree.heading(columns, text=columns)
            else:
                for column in columns:
                    self.tree.heading(column, text=column)

        self.query_box.pack(fill=tk.X, expand=False, pady=10)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.query_box.bind(
            '<KeyRelease>',
            lambda e: self.search_by_query(
                self.query_box.get('1.0', 'end-1c')
            )
        )

    def update_tree(self, new_rows: list[list]) -> None:
        """Updates the tree with new rows"""

        for row in self.tree.get_children():
            self.tree.delete(row)

        for new_row in new_rows:
            new_row = (new_row,)
            self.tree.insert('', tk.END, values=new_row)

    def search_by_query(self, query: str) -> None:
        """Searches the tree for the query and selects (by highlighting) the matching rows"""

        selections = [
            child
            for child in self.tree.get_children()
            if query.lower() in self.tree.item(child)['values'][0].lower()
        ]

        self.tree.selection_set(selections)

    def get_selected_row(self) -> tuple:
        """Returns the selected row"""

        selected_rows = [
            self.tree.item(el)['values'][0]
            for el in self.tree.selection()
        ]

        return selected_rows


class DashBoardView(tk.Frame):
    def __init__(self, master: tk.Tk | tk.Frame, **karws):

        tk.Frame.__init__(
            self,
            master=master,
        )

    def setup(self, labels: list[str], entries: list[str]) -> None:
        """Sets up the dashboard"""

        self.define_labels(labels)
        self.define_entries(entries)

    def define_labels(self, labels: list[str]) -> None:
        """Defines the labels for the dashboard"""

        self.labels = {}

        for index, label in enumerate(labels):
            self.labels[label] = tk.Label(
                self,
                text=label
            )

            self.labels[label].grid(row=index, column=0, sticky='W')

    def define_entries(self, entries: list[str]) -> None:
        """Defines the entries for the dashboard"""

        self.entries = {}

        for index, entry in enumerate(entries):
            self.entries[entry] = tk.Entry(
                self,
                width=15
            )

            self.entries[entry].grid(row=index, column=1, sticky='WE')

    def update_entries(self, data: dict[str, str]) -> None:

        for self_entry in self.entries:
            self.entries[self_entry].delete(0, tk.END)

        for key, value in data.items():
            self.entries[key].insert(0, value)

    def get_entries(self) -> dict[str, str]:

        return {
            key: self.entries[key].get()
            for key in self.entries
        }


class DashBoardHCView(tk.Frame):
    def __init__(self, master: tk.Tk | tk.Frame, **karws):

        # Map attributes
        # name
        # scale
        # equidistance
        # grivation
        # geographic_coordinates
        # export_boundaries
        # notes
        # author
        # private

        # Files paths
        # map_file
        # imp_file
        # pdf_file
        # gif_file

        tk.Frame.__init__(
            self,
            master=master,
        )

        self.section_title_1 = tk.Label(self, text='Map Attributes')

        self.name = tk.Label(self, text='Name')
        self.name_field = tk.Entry(self, state=tk.DISABLED)

        self.scale = tk.Label(self, text='Scale')
        self.scale_field = tk.Entry(self, state=tk.DISABLED)

        self.equidistance = tk.Label(self, text='Equidistance')
        self.equidistance_field = ttk.Combobox(
            self, values=[str(eq) for eq in [2, 2.5, 5, 10, 15, 50]],)

        self.grivation = tk.Label(self, text='Grivation')
        self.grivation_field = tk.Entry(self, state=tk.DISABLED)

        self.geographic_coordinates = tk.Label(self, text='Center Coordinates')
        self.geographic_coordinates_field = tk.Entry(self, state=tk.DISABLED)

        self.export_boundaries = tk.Label(self, text='Export Coordinates')
        self.export_boundaries_field = tk.Entry(self, state=tk.DISABLED)

        self.notes = tk.Label(self, text='Notes')
        self.notes_field = tk.Text(self, height=15, state=tk.DISABLED)

        self.author = tk.Label(self, text='Author')
        self.author_field = tk.Listbox(self, selectmode=tk.MULTIPLE, height=3)

        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)

        self.section_title_2 = tk.Label(self, text='Files Paths')

        self.map_file = tk.Label(self, text='Map file')
        self.map_file_field = tk.Entry(self, state=tk.DISABLED)

        self.imp_file = tk.Label(self, text='Imp file')
        self.imp_file_field = tk.Entry(self, state=tk.DISABLED)

        self.pdf_file = tk.Label(self, text='Pdf file')
        self.pdf_file_field = tk.Entry(self, state=tk.DISABLED)

        self.gif_file = tk.Label(self, text='Gif file')
        self.gif_file_field = tk.Entry(self, state=tk.DISABLED)

        self.author_field.insert(
            tk.END,
            'Tommaso Bocchietti',
            'Filippo Moscatelli'
        )

        self.var1 = tk.IntVar()
        self.private = tk.Checkbutton(
            self,
            text='Private',
            variable=self.var1,
            onvalue=1,
            offvalue=0
        )

        self.section_title_1.grid(row=0, column=0, sticky='W')
        self.name.grid(row=1, column=0, sticky='W')
        self.name_field.grid(row=1, column=1, sticky='WE')
        self.scale.grid(row=2, column=0, sticky='W')
        self.scale_field.grid(row=2, column=1, sticky='WE')
        self.equidistance.grid(row=3, column=0, sticky='W')
        self.equidistance_field.grid(row=3, column=1, sticky='WE')
        self.grivation.grid(row=4, column=0, sticky='W')
        self.grivation_field.grid(row=4, column=1, sticky='WE')

        self.geographic_coordinates.grid(row=5, column=0, sticky='W')
        self.geographic_coordinates_field.grid(row=5, column=1, sticky='WE')

        self.export_boundaries.grid(row=6, column=0, sticky='W')
        self.export_boundaries_field.grid(row=6, column=1, sticky='WE')

        self.notes.grid(row=7, column=0, sticky='W')
        self.notes_field.grid(row=7, column=1, sticky='WE')
        self.author.grid(row=8, column=0, sticky='W')
        self.author_field.grid(row=8, column=1, sticky='WE')
        self.private.grid(row=9, column=0, sticky='W')

        self.separator.grid(row=10, column=0, columnspan=2,
                            sticky='WE', pady=30)

        self.section_title_2.grid(row=11, column=0, sticky='W')
        self.map_file.grid(row=12, column=0, sticky='W')
        self.map_file_field.grid(row=12, column=1, sticky='WE')
        self.imp_file.grid(row=13, column=0, sticky='W')
        self.imp_file_field.grid(row=13, column=1, sticky='WE')
        self.pdf_file.grid(row=14, column=0, sticky='W')
        self.pdf_file_field.grid(row=14, column=1, sticky='WE')
        self.gif_file.grid(row=15, column=0, sticky='W')
        self.gif_file_field.grid(row=15, column=1, sticky='WE')

        self.columnconfigure(1, weight=1)

    def enable(self) -> None:

        self.name_field.config(state=tk.NORMAL)
        self.scale_field.config(state=tk.NORMAL)
        self.grivation_field.config(state=tk.NORMAL)
        self.geographic_coordinates_field.config(state=tk.NORMAL)
        self.export_boundaries_field.config(state=tk.NORMAL)
        self.notes_field.config(state=tk.NORMAL)
        self.map_file_field.config(state=tk.NORMAL)
        self.imp_file_field.config(state=tk.NORMAL)
        self.pdf_file_field.config(state=tk.NORMAL)
        self.gif_file_field.config(state=tk.NORMAL)

    def disable(self) -> None:

        self.name_field.config(state=tk.DISABLED)
        self.scale_field.config(state=tk.DISABLED)
        self.grivation_field.config(state=tk.DISABLED)
        self.geographic_coordinates_field.config(state=tk.DISABLED)
        self.export_boundaries_field.config(state=tk.DISABLED)
        self.notes_field.config(state=tk.DISABLED)
        self.map_file_field.config(state=tk.DISABLED)
        self.imp_file_field.config(state=tk.DISABLED)
        self.pdf_file_field.config(state=tk.DISABLED)
        self.gif_file_field.config(state=tk.DISABLED)

    def clear(self) -> None:

        self.enable()

        self.name_field.delete(0, tk.END)
        self.scale_field.delete(0, tk.END)
        self.grivation_field.delete(0, tk.END)
        self.equidistance_field.set('')
        self.export_boundaries_field.delete(0, tk.END)
        self.geographic_coordinates_field.delete(0, tk.END)
        self.notes_field.delete('1.0', tk.END)
        self.map_file_field.delete(0, tk.END)
        self.imp_file_field.delete(0, tk.END)
        self.pdf_file_field.delete(0, tk.END)
        self.gif_file_field.delete(0, tk.END)

        self.disable()

    def get_entries(self) -> dict[str, str | int]:

        return {
            'name': self.name_field.get(),
            'scale': self.scale_field.get(),
            'equidistance': self.equidistance_field.get(),
            'grivation': self.grivation_field.get(),
            'geographic_coordinates': self.geographic_coordinates_field.get(),
            'export_boundaries': self.export_boundaries_field.get(),
            'notes': self.notes_field.get('1.0', tk.END),
            'author': self.author_field.get(tk.ACTIVE),
            'private': self.var1.get(),
            'map_file': self.map_file_field.get(),
            'imp_file': self.imp_file_field.get(),
            'pdf_file': self.pdf_file_field.get(),
            'gif_file': self.gif_file_field.get()
        }

    def update_entries(self, data: dict[str, str]) -> None:

        self.clear()
        self.enable()

        for key, value in data.items():
            if key in ['name', 'scale', 'grivation', 'geographic_coordinates', 'export_boundaries', 'map_file', 'imp_file', 'pdf_file', 'gif_file']:
                self.__dict__[key + '_field'].insert(0, value)

            elif key == 'equidistance':
                self.equidistance_field.set(value)

            elif key == 'notes':
                self.notes_field.insert('1.0', value)

        self.disable()
