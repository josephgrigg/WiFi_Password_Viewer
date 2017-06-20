import tkinter as tk
import tkinter.ttk as ttk
from column_select_window import ColumnSelect
from data import Data


class MainScreen:

    def __init__(self, master):
        self.root = master
        self.mainframe = ttk.Frame(self.root, padding=(3, 3, 0, 0))
        self.mainframe.grid(row=0, column=0, sticky='NSEW')
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.mainframe.grid_rowconfigure(0, weight=1)
        # Add an area to display the information gathered about the networks.
        self.refresh_results_display()

    def multi_column_listbox(self, column_names):
        tree = ttk.Treeview(columns=column_names, show='headings')

        for col in tree['columns']:
            tree.column(col, width=300)
            if col == 'Encryption' or col == 'Authentication':
                tree.column(col, width=100)
            tree.heading(col, text=col, anchor='center',
                         command=lambda x=col: self.sort_column(tree, x, False))
        return tree

    def fill_multi_column_listbox(self, listbox, data):
        grey = False

        for network_info in data:
            if not grey:
                listbox.insert('', index='end', values=network_info)
            else:
                listbox.insert('', index='end', values=network_info,
                               tags=['grey background'])
            grey = not grey

    def sort_column(self, tree, column, reverse_sort_flag):
        # column_values will be a list of tuples (x, row) where x is
        # the value at the given row in the column to be sorted.
        values = [(tree.set(row, column), row) for row in tree.get_children('')]
        values.sort(reverse=reverse_sort_flag)

        for index, item in enumerate(values):
            tree.move(item[1], '', index)

        tree.heading(
            column,
            command=lambda x=column: self.sort_column(tree, x, not reverse_sort_flag))

    def refresh_results_display(self):
        network_data = Data().network_info
        vert_sb = ttk.Scrollbar(self.mainframe, orient=tk.VERTICAL)
        horz_sb = ttk.Scrollbar(self.mainframe, orient=tk.HORIZONTAL)
        self.results_display = self.multi_column_listbox(ColumnSelect.column_names)
        self.fill_multi_column_listbox(self.results_display, network_data)
        self.results_display.grid(row=0, column=0, in_=self.mainframe,
                                  sticky='NSEW')
        self.results_display.configure(yscrollcommand=vert_sb.set,
                                       xscrollcommand=horz_sb.set)
        vert_sb.grid(row=0, column=1, sticky="NS")
        vert_sb.config(command=self.results_display.yview)
        horz_sb.grid(row=1, column=0, sticky="EW")
        horz_sb.config(command=self.results_display.xview)
        self.results_display['displaycolumns'] = ColumnSelect.columns_shown

    def select_all(self):
        """ :type results_display: tkinter.ttk.treeview object """
        self.results_display.selection_set(self.results_display.get_children())

    def deselect_all(self):
        self.results_display.selection_set([])

    def invert_selection(self):
        self.results_display.selection_toggle(self.results_display.get_children())
