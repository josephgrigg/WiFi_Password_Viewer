import tkinter as tk
from column_select_window import ColumnSelect
from about_window import About
from data import Data
import gui_functions as gf


class MenuBar(tk.Menu):

    def __init__(self, master, screen):
        # Initialize menu bar and drop down menus.
        self.root = master
        super().__init__(self.root)
        self.screen = screen
        self.grey_rows = False
        menu_file = tk.Menu(self)
        menu_edit = tk.Menu(self)
        menu_view = tk.Menu(self)
        menu_preferences = tk.Menu(self)
        menu_help = tk.Menu(self)
        self.root.config(menu=self)

        # Add drop down menus to menu bar.
        self.add_cascade(menu=menu_file, label='File')
        self.add_cascade(menu=menu_edit, label='Edit')
        self.add_cascade(menu=menu_view, label='View')
        self.add_cascade(menu=menu_preferences, label='Preferences')
        self.add_cascade(menu=menu_help, label='Help')

        # Add options for File menu.
        menu_file.add_command(
            label='Save Selection (tab delimited)',
            command=lambda: gf.save_as(self.screen.results_display),
            accelerator='Ctrl+S')

        # Add options for View menu.
        row_color = tk.StringVar()
        """
        menu_view.add_checkbutton(
            label='Color Odd Rows Grey',
            variable=row_color, onvalue='light grey', offvalue='white',
            command=lambda c=row_color: gf.toggle_row_color(self, c))
        """
        menu_view.add_command(
            label='Show/Hide Columns',
            command=lambda: ColumnSelect(self.screen.results_display))

        # Add options for Edit menu.
        menu_edit.add_command(
            label='Copy Selection',
            command=lambda: gf.copy_selection(self.root, self.screen.results_display),
            accelerator='Ctrl+C')
        """
        menu_edit.add_command(
            label='Copy Current Network Password',
            command=NotImplemented)
        """
        menu_edit.add_command(
            label='Clear Clipboard',
            command=lambda: gf.clear_clipboard(self.root))
        menu_edit.add_separator()
        menu_edit.add_command(
            label='Select All',
            command=lambda: self.screen.select_all(),
            accelerator='Ctrl+A')
        menu_edit.add_command(
            label='Deselect All',
            command=lambda: self.screen.deselect_all(),
            accelerator='Ctrl+D')
        menu_edit.add_command(
            label='Invert Selection',
            command=lambda: self.screen.invert_selection(),
            accelerator='Ctrl+I')
        menu_edit.add_separator()
        menu_edit.add_command(
            label='Refresh',
            command=lambda: self.screen.refresh_results_display(),
            accelerator='F5')

        # Add options for Preferences menu.
        decryption_method_menu = tk.Menu(self)
        menu_preferences.add_cascade(label='Decryption Method',
                                     menu=decryption_method_menu)
        decryption_method_menu.add_radiobutton(label='Parse Command Prompt',
                                               command=self.update_method1)
        decryption_method_menu.add_radiobutton(label='Decrypt from XML files',
                                               command=self.update_method2)
        decryption_method_menu.invoke(1)

        # Add options for Help menu.
        menu_help.add_command(label='About', command=lambda: About(self.root))

    def update_method1(self):
        Data.data_collection_method = 'cmd'

    def update_method2(self):
        Data.data_collection_method = 'xml'


class PopupMenu(tk.Menu):

    def __init__(self, master, screen):
        self.root = master
        self.screen = screen
        super().__init__(self.root)
        # Add a right click menu.
        self.screen.mainframe.bind_all('<Button-3>', self.popup_menu)
        self.add_command(
            label='Copy Selection',
            command=lambda: gf.copy_selection(self.root, self.screen.results_display))
        self.add_separator()
        self.add_command(
            label='Select All',
            command=lambda: self.screen.select_all())
        self.add_command(
            label='Deselect All',
            command=lambda: self.screen.deselect_all())
        self.add_command(
            label='Invert Selection',
            command=lambda: self.screen.invert_selection())
        self.add_separator()
        self.add_command(
            label='Refresh',
            command=lambda: self.screen.refresh_results_display())
        self.add_command(
            label='Save Selection',
            command=lambda: gf.save_as(self.screen.results_display))

    def popup_menu(self, event):
        self.post(event.x_root, event.y_root)
