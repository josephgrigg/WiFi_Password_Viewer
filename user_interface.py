# Tkinter in python 2, tkinter in python 3
import tkinter as tk
from mainscreen import MainScreen
import menus
import gui_functions as gf


class ProgramGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.option_add('*tearOff', tk.FALSE)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title('WiFi Password Revealer')
        self.screen = MainScreen(self)
        self.menu_bar = menus.MenuBar(self, self.screen)
        self.right_click_menu = menus.PopupMenu(self, self.screen)

        # Keyboard shortcuts
        self.bind_all('<Control-c>',
                      lambda event=None: gf.copy_selection(self, self.screen.results_display))
        self.bind_all('<F5>',
                      lambda event=None: self.screen.refresh_results_display())
        self.bind_all('<Control-a>',
                      lambda event=None: self.screen.select_all())
        self.bind_all('<Control-d>',
                      lambda event=None: self.screen.deselect_all())
        self.bind_all('<Control-i>',
                      lambda event=None: self.screen.invert_selection())
        self.bind_all('<Control-s>',
                      lambda event=None: gf.save_as(self.screen.results_display))


if __name__ == "__main__":
    # Initialize the network information to appear when program is first loaded.
    # network_data = Data(data_collection_method).network_info
    my_gui = ProgramGUI()
    my_gui.mainloop()
