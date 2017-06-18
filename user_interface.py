# Tkinter in python 2, tkinter in python 3
from tkinter import filedialog
import tkinter as tk
import tkinter.ttk as ttk
from cmd_prompt_method import get_networks_and_pwds
import subprocess
import pickle
import sys
import os


program_title = 'WiFi Password Revealer'
program_directory = sys.path[0]
os.chdir(program_directory)
data_collection_method = 'xml'


class Data:

    def __init__(self, pwd_collection_method):
        self.network_info = self.collect_network_info(pwd_collection_method)

    def collect_network_info(self, pwd_collection_method):
        if pwd_collection_method == 'cmd':
            data = get_networks_and_pwds()

        elif pwd_collection_method == 'xml':
            # Decrypt the XML wifi passwords under System context.
            subprocess.call('psexec.exe -i -s cmd.exe /c \"cd \"%s\" & python xml_decryption_method.py\"' % program_directory)
            # Load the pickled network data that was just saved.
            with open('data_pickle.p', 'rb') as pfile:
                data = pickle.load(pfile)
            # Delete the pickle file after it has been loaded.
            os.remove('data_pickle.p')

        else:
            data = []

        return data


class ColumnSelect:
    column_names = ['Network', 'Password', 'Authentication', 'Encryption', 'Filename']
    column_order = ['Network', 'Password', 'Authentication', 'Encryption', 'Filename']
    columns = {'Network': True, 'Password': True, 'Authentication': True, 'Encryption': True, 'Filename': True}
    columns_shown = column_names

    def __init__(self, results_display):
        self.results_display = results_display
        self.top = tk.Toplevel()
        self.top.title("Show/Hide Columns")
        self.networks = tk.BooleanVar(value=ColumnSelect.columns['Network'])
        self.passwords = tk.BooleanVar(value=ColumnSelect.columns['Password'])
        self.auths = tk.BooleanVar(value=ColumnSelect.columns['Authentication'])
        self.encryptions = tk.BooleanVar(value=ColumnSelect.columns['Encryption'])
        self.filenames = tk.BooleanVar(value=ColumnSelect.columns['Filename'])
        self.msg = tk.Message(self.top, text='Select which columns you would like to be displayed.')
        self.msg.grid(in_=self.top, row=0)
        self.network = tk.Checkbutton(self.top, text='Network', variable=self.networks)
        self.password = tk.Checkbutton(self.top, text='Password', variable=self.passwords)
        self.auth = tk.Checkbutton(self.top, text='Authentication', variable=self.auths)
        self.encrypt = tk.Checkbutton(self.top, text='Encryption', variable=self.encryptions)
        self.fnames = tk.Checkbutton(self.top, text='Filename', variable=self.filenames)
        self.submit_button = tk.Button(self.top, text='Submit', command=self.submit_changes)
        self.cancel_button = tk.Button(self.top, text='Cancel', command=self.top.destroy)
        self.network.grid(in_=self.top, row=1, sticky='W')
        self.password.grid(in_=self.top, row=2, sticky='W')
        self.auth.grid(in_=self.top, row=3, sticky='W')
        self.encrypt.grid(in_=self.top, row=4, sticky='W')
        self.fnames.grid(in_=self.top, row=5, sticky='W')
        self.submit_button.grid(in_=self.top, row=6, column=0, sticky='E')
        self.cancel_button.grid(in_=self.top, row=6, column=1, sticky='E')

    def submit_changes(self):
        ColumnSelect.columns['Network'] = self.networks.get()
        ColumnSelect.columns['Password'] = self.passwords.get()
        ColumnSelect.columns['Authentication'] = self.auths.get()
        ColumnSelect.columns['Encryption'] = self.encryptions.get()
        ColumnSelect.columns['Filename'] = self.filenames.get()
        ColumnSelect.columns_shown = []
        for name in ColumnSelect.column_order:
            if ColumnSelect.columns[name]:
                ColumnSelect.columns_shown.append(name)
        self.results_display['displaycolumns'] = ColumnSelect.columns_shown
        self.top.destroy()


class MenuBar:

    def __init__(self, master, screen):
        # Initialize menu bar and drop down menus.
        self.root = master
        self.screen = screen
        self.grey_rows = False
        menu_bar = tk.Menu(master)
        menu_file = tk.Menu(menu_bar)
        menu_edit = tk.Menu(menu_bar)
        menu_view = tk.Menu(menu_bar)
        menu_preferences = tk.Menu(menu_bar)
        self.root.config(menu=menu_bar)

        # Add drop down menus to menu bar.
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.add_cascade(menu=menu_edit, label='Edit')
        menu_bar.add_cascade(menu=menu_view, label='View')
        menu_bar.add_cascade(menu=menu_preferences, label='Preferences')

        # Add options for File menu.
        menu_file.add_command(label='Save Selection (tab delimited)',
                              command=self.save_as,
                              accelerator='Ctrl+S')

        # Add options for View menu.
        row_color = tk.StringVar()
        menu_view.add_checkbutton(
            label='Color Odd Rows Grey',
            variable=row_color, onvalue='light grey', offvalue='white',
            command=lambda c=row_color: self.toggle_row_color(c))
        menu_view.add_command(label='Show/Hide Columns',
                              command=self.column_selection_window)

        # Add options for Edit menu.
        menu_edit.add_command(label='Copy Selection',
                              command=self.copy_selection,
                              accelerator='Ctrl+C')
        menu_edit.add_command(label='Copy Current Network Password',
                              command=NotImplemented)
        menu_edit.add_command(label='Clear Clipboard',
                              command=self.clear_clipboard)
        menu_edit.add_separator()
        menu_edit.add_command(label='Select All',
                              command=self.select_all,
                              accelerator='Ctrl+A')
        menu_edit.add_command(label='Deselect All',
                              command=self.deselect_all,
                              accelerator='Ctrl+D')
        menu_edit.add_command(label='Invert Selection',
                              command=self.invert_selection,
                              accelerator='Ctrl+I')
        menu_edit.add_separator()
        menu_edit.add_command(label='Refresh',
                              command=self.refresh_data,
                              accelerator='F5')

        # Add options for Preferences menu.
        decryption_method_menu = tk.Menu(menu_bar)
        menu_preferences.add_cascade(
            label='Decryption Method', menu=decryption_method_menu)
        decryption_method_menu.add_radiobutton(
            label='Parse Command Prompt',
            command=lambda: globals().update(data_collection_method='cmd'))
        decryption_method_menu.add_radiobutton(
            label='Decrypt from XML files',
            command=lambda: globals().update(data_collection_method='xml'))
        decryption_method_menu.invoke(1)

    def save_as(self):
        file = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        # Exit function if user presses cancel button.
        if file is None:
            return
        # Determine the order that the columns appear on the screen.
        order_map = []
        # '#all' means that the columns are in their original order and all
        # are being shown.
        if '#all' in self.screen.results_display['displaycolumns']:
            order_map = list(range(len(ColumnSelect.column_names)))
        else:
            for title in self.screen.results_display['displaycolumns']:
                order_map.append(ColumnSelect.column_names.index(title))

        for item in self.screen.results_display.selection():
            values = self.screen.results_display.item(item=item, option='values')
            for i in range(len(order_map)):
                if order_map[i] < len(values):
                    file.write(values[order_map[i]])
                    if i != len(order_map) - 1:
                        file.write('\t')
            if item != self.screen.results_display.selection()[-1]:
                file.write('\n')
        file.close()

    def column_selection_window(self):
        ColumnSelect(self.screen.results_display)

    def toggle_row_color(self, row_color):
        self.screen.results_display.tag_configure('grey background',
                                                background=row_color.get())
        self.grey_rows = not self.grey_rows

    def select_all(self):
        self.screen.results_display.selection_set(
            self.screen.results_display.get_children())

    def deselect_all(self):
        self.screen.results_display.selection_set([])

    def invert_selection(self):
        self.screen.results_display.selection_toggle(
            self.screen.results_display.get_children())

    def copy_selection(self):
        self.root.clipboard_clear()

        # Determine the order that the columns appear on the screen.
        order_map = []
        # '#all' means that the columns are in their original order and all
        # are being shown.
        if '#all' in self.screen.results_display['displaycolumns']:
            order_map = list(range(len(ColumnSelect.column_names)))
        else:
            for title in self.screen.results_display['displaycolumns']:
                order_map.append(ColumnSelect.column_names.index(title))

        for item in self.screen.results_display.selection():
            values = self.screen.results_display.item(item=item, option='values')
            for i in range(len(order_map)):
                if order_map[i] < len(values):
                    self.root.clipboard_append(values[order_map[i]])
                    if i != len(order_map) - 1:
                        self.root.clipboard_append('\t')
            if item != self.screen.results_display.selection()[-1]:
                self.root.clipboard_append('\n')

    def clear_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append('')

    def refresh_data(self):
        self.screen.refresh_results_display()

        if self.grey_rows:
            self.screen.results_display.tag_configure('grey background',
                                                    background='light grey')


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
        network_data = Data(data_collection_method).network_info
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


class ProgramGUI(tk.Tk):

    def __init__(self, master):
        self.root = master
        self.root.option_add('*tearOff', tk.FALSE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.title(program_title)
        self.screen = MainScreen(self.root)
        self.menu_bar = MenuBar(self.root, self.screen)

    # Keyboard shortcuts
        self.root.bind_all('<Control-c>', self.copy_shortcut)
        self.root.bind_all('<F5>', self.refresh_shortcut)
        self.root.bind_all('<Control-a>', self.select_all_shortcut)
        self.root.bind_all('<Control-d>', self.deselect_all_shortcut)
        self.root.bind_all('<Control-i>', self.invert_selection_shortcut)
        self.root.bind_all('<Control-s>', self.save_shortcut)

    def copy_shortcut(self, event):
        self.menu_bar.copy_selection()

    def refresh_shortcut(self, event):
        self.menu_bar.refresh_data()

    def select_all_shortcut(self, event):
        self.menu_bar.select_all()

    def deselect_all_shortcut(self, event):
        self.menu_bar.deselect_all()

    def invert_selection_shortcut(self, event):
        self.menu_bar.invert_selection()

    def save_shortcut(self, event):
        self.menu_bar.save_as()


if __name__ == "__main__":
    root = tk.Tk()
    # Initialize the network information to appear when program is first loaded.
    # network_data = Data(data_collection_method).network_info
    my_gui = ProgramGUI(root)
    root.mainloop()
