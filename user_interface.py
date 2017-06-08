# Tkinter in python 2, tkinter in python 3
import tkinter as tk
import tkinter.ttk as ttk
from cmd_prompt_method2 import get_networks_and_pwds


program_title = 'WiFi Password Revealer'
data = get_networks_and_pwds()
column_names = ['Network', 'Password', 'Authentication']


class menu_bar:

	def __init__(self, master, result_display):
		self.root = master
		self.result_display = result_display
		menu_bar = tk.Menu(master)
		menu_file = tk.Menu(menu_bar)
		menu_edit = tk.Menu(menu_bar)
		menu_view = tk.Menu(menu_bar)
		menu_preferences = tk.Menu(menu_bar)
		menu_bar.add_cascade(menu=menu_file, label='File')
		menu_bar.add_cascade(menu=menu_edit, label='Edit')
		menu_bar.add_cascade(menu=menu_view, label='View')
		menu_bar.add_cascade(menu=menu_preferences, label='Preferences')
		menu_file.add_command(label='Export')
		row_color = tk.StringVar()
		menu_view.add_checkbutton(label='Color Odd Rows Grey',
			variable=row_color, onvalue='light grey', offvalue='white',
			command=lambda c=row_color: self.toggle_row_color(c))

		menu_edit.add_command(label='Copy Selection',
							command=self.copy_selection)  # Implement
		menu_edit.add_command(label='Copy Current Network Password')  # Implement
		menu_edit.add_command(label='Mark All', command=self.mark_all)
		menu_edit.add_command(label='Unmark All', command=self.unmark_all)
		master.config(menu=menu_bar)

	def toggle_row_color(self, row_color):
		self.result_display.tag_configure('grey background',
										background=row_color.get())

	def mark_all(self):
		self.result_display.selection_set(self.result_display.get_children())

	def unmark_all(self):
		self.result_display.selection_set([])

	def copy_selection(self):
		self.root.clipboard_clear()
		for item in self.result_display.selection():
			values = self.result_display.item(item=item, option='values')
			self.root.clipboard_append(values[0] + '\t' + values[1] + '\n')


class main_screen:

	def __init__(self, master):
		self.root = master

		mainframe = ttk.Frame(self.root, padding=(3, 3, 0, 0))
		mainframe.grid(row=0, column=0, sticky='NSEW')
		mainframe.grid_columnconfigure(0, weight=1)
		mainframe.grid_rowconfigure(0, weight=1)

		# Add an area to display the information gathered about the networks.
		vert_sb = ttk.Scrollbar(mainframe, orient=tk.VERTICAL)
		horz_sb = ttk.Scrollbar(mainframe, orient=tk.HORIZONTAL)
		self.result_display = self.multi_column_listbox(column_names)
		self.fill_multi_column_listbox(self.result_display, data)
		self.result_display.grid(row=0, column=0, in_=mainframe, sticky='NSEW')
		self.result_display.configure(yscrollcommand=vert_sb.set,
			xscrollcommand=horz_sb.set)
		vert_sb.grid(row=0, column=1, sticky="NS")
		vert_sb.config(command=self.result_display.yview)
		horz_sb.grid(row=1, column=0, sticky="EW")
		horz_sb.config(command=self.result_display.xview)

	def multi_column_listbox(self, column_names):
		tree = ttk.Treeview(columns=column_names, show='headings')
		for col in tree['columns']:
			tree.column(col, width=300)
			tree.heading(col, text=col, anchor='center')

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


class program_GUI:

	def __init__(self, master):
		self.root = master
		self.root.option_add('*tearOff', tk.FALSE)
		self.root.columnconfigure(0, weight=1)
		self.root.rowconfigure(0, weight=1)
		self.root.title(program_title)
		self.screen = main_screen(self.root)
		self.menu_bar = menu_bar(self.root, self.screen.result_display)
		# self.screen.result_display['displaycolumns'] = ('Password')
		# print(len(self.screen.result_display['displaycolumns']))


if __name__ == "__main__":
	root = tk.Tk()
	my_gui = program_GUI(root)
	root.mainloop()
