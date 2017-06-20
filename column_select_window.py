import tkinter as tk


class ColumnSelect(tk.Toplevel):
    column_names = ['Network', 'Password', 'Authentication', 'Encryption', 'Filename']
    column_order = ['Network', 'Password', 'Authentication', 'Encryption', 'Filename']
    columns = {'Network': True, 'Password': True, 'Authentication': True, 'Encryption': True, 'Filename': True}
    columns_shown = column_names

    def __init__(self, results_display):
        super().__init__()
        self.results_display = results_display
        self.title("Show/Hide Columns")
        self.networks = tk.BooleanVar(value=ColumnSelect.columns['Network'])
        self.passwords = tk.BooleanVar(value=ColumnSelect.columns['Password'])
        self.auths = tk.BooleanVar(value=ColumnSelect.columns['Authentication'])
        self.encryptions = tk.BooleanVar(value=ColumnSelect.columns['Encryption'])
        self.filenames = tk.BooleanVar(value=ColumnSelect.columns['Filename'])
        self.msg = tk.Message(self, text='Select which columns you would like to be displayed.')
        self.msg.grid(in_=self, row=0)
        self.network = tk.Checkbutton(self, text='Network', variable=self.networks)
        self.password = tk.Checkbutton(self, text='Password', variable=self.passwords)
        self.auth = tk.Checkbutton(self, text='Authentication', variable=self.auths)
        self.encrypt = tk.Checkbutton(self, text='Encryption', variable=self.encryptions)
        self.fnames = tk.Checkbutton(self, text='Filename', variable=self.filenames)
        self.submit_button = tk.Button(self, text='Submit', command=self.submit_changes)
        self.cancel_button = tk.Button(self, text='Cancel', command=self.destroy)
        self.network.grid(in_=self, row=1, sticky='W')
        self.password.grid(in_=self, row=2, sticky='W')
        self.auth.grid(in_=self, row=3, sticky='W')
        self.encrypt.grid(in_=self, row=4, sticky='W')
        self.fnames.grid(in_=self, row=5, sticky='W')
        self.submit_button.grid(in_=self, row=6, column=0, sticky='E')
        self.cancel_button.grid(in_=self, row=6, column=1, sticky='E')

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
        self.destroy()
