# Tkinter in python 2, tkinter in python 3
import tkinter as tk
import tkinter.ttk as ttk
from cmd_prompt_method import get_networks_and_pwds
import subprocess
import pickle
import sys
import os


program_title = 'WiFi Password Revealer'
column_names = ['Network', 'Password', 'Authentication']
program_directory = sys.path[0]
os.chdir(program_directory)
data_collection_method = 'cmd'


class data:

	def __init__(self, pwd_collection_method):
		self.network_info = self.collect_network_info(pwd_collection_method)

	def collect_network_info(self, pwd_collection_method):
		if pwd_collection_method == 'cmd':
			data = get_networks_and_pwds()

		elif pwd_collection_method == 'xml':
			# Decrypt the XML wifi passwords under System context.
			subprocess.call('psexec.exe -i -s cmd.exe /c \"cd \"%s\" & python xml_decryption_method.py\"' % program_directory)
			# Load the pickled network data that was just saved.
			with open('pickle-example.p', 'rb') as pfile:
				data_dictionary = pickle.load(pfile)
			data = []
			for key in data_dictionary.keys():
				data.append((key, data_dictionary[key]))
			# Delete the pickle file after it has been loaded.
			os.remove('pickle-example.p')

		else:
			data = []

		return data


class menu_bar:

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
		menu_file.add_command(label='Export', command=NotImplemented)

		# Add options for View menu.
		row_color = tk.StringVar()
		menu_view.add_checkbutton(label='Color Odd Rows Grey',
			variable=row_color, onvalue='light grey', offvalue='white',
			command=lambda c=row_color: self.toggle_row_color(c))

		# Add options for Edit menu.
		menu_edit.add_command(label='Copy Selection',
			command=self.copy_selection)
		menu_edit.add_command(label='Copy Current Network Password', command=NotImplemented)
		menu_edit.add_command(label='Mark All', command=self.mark_all)
		menu_edit.add_command(label='Unmark All', command=self.unmark_all)
		menu_edit.add_command(label='Refresh', command=self.refresh_data)

		# Add options for Preferences menu.
		decryption_method_menu = tk.Menu(menu_bar)
		menu_preferences.add_cascade(label='Decryption Method', menu=decryption_method_menu)
		decryption_method_menu.add_radiobutton(label='Parse Command Prompt',
			command=lambda: globals().update(data_collection_method='cmd'))
		decryption_method_menu.add_radiobutton(label='Decrypt from XML files',
			command=lambda: globals().update(data_collection_method='xml'))

	def toggle_row_color(self, row_color):
		self.screen.result_display.tag_configure('grey background',
			background=row_color.get())
		self.grey_rows = not self.grey_rows

	def mark_all(self):
		self.screen.result_display.selection_set(self.screen.result_display.get_children())

	def unmark_all(self):
		self.screen.result_display.selection_set([])

	def copy_selection(self):
		self.root.clipboard_clear()
		for item in self.screen.result_display.selection():
			values = self.screen.result_display.item(item=item, option='values')
			self.root.clipboard_append(values[0] + '\t' + values[1] + '\n')

	def refresh_data(self):
		self.screen.refresh_results_display()
		if self.grey_rows:
			self.screen.result_display.tag_configure('grey background',
				background='light grey')


class main_screen:

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
		tree.heading(column, command=lambda x=column: self.sort_column(tree, x, not reverse_sort_flag))

	def refresh_results_display(self):
		network_data = data(data_collection_method).network_info
		vert_sb = ttk.Scrollbar(self.mainframe, orient=tk.VERTICAL)
		horz_sb = ttk.Scrollbar(self.mainframe, orient=tk.HORIZONTAL)
		self.result_display = self.multi_column_listbox(column_names)
		self.fill_multi_column_listbox(self.result_display, network_data)
		self.result_display.grid(row=0, column=0, in_=self.mainframe, sticky='NSEW')
		self.result_display.configure(yscrollcommand=vert_sb.set,
			xscrollcommand=horz_sb.set)
		vert_sb.grid(row=0, column=1, sticky="NS")
		vert_sb.config(command=self.result_display.yview)
		horz_sb.grid(row=1, column=0, sticky="EW")
		horz_sb.config(command=self.result_display.xview)


class program_GUI:

	def __init__(self, master):
		self.root = master
		self.root.option_add('*tearOff', tk.FALSE)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		self.root.title(program_title)
		self.screen = main_screen(self.root)
		self.menu_bar = menu_bar(self.root, self.screen)
		# self.screen.result_display['displaycolumns'] = ('Password')
		# print(len(self.screen.result_display['displaycolumns']))


# Initialize the network information to appear when program is first loaded.
network_data = data(data_collection_method).network_info

if __name__ == "__main__":
	root = tk.Tk()
	my_gui = program_GUI(root)
	root.mainloop()
