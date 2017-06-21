import tkinter as tk
import tkinter.ttk as ttk
import webbrowser


class About(tk.Toplevel):

    def __init__(self, master):
        self.root = master
        super().__init__(self.root)
        self.wm_resizable(width=False, height=False)
        self.title('About')
        self.wm_attributes('-toolwindow', True)
        self.grab_set()
        self.frame = ttk.Frame(self)
        self.frame.pack()
        self.msg = tk.Message(
            self.frame,
            text='WiFi Password Revealer is a work in progress.',
            width=300)
        self.msg2 = tk.Message(
            self.frame,
            text='For help and information, please visit the project\'s Github page.',
            width=300)
        self.link = tk.Label(
            self.frame,
            text=r'www.github.com/jgrigg2017/WiFi_Password_Viewer',
            fg='blue',
            cursor='hand2')
        self.link.bind(
            '<Button-1>',
            lambda event=None: webbrowser.open_new(event.widget.cget('text')))
        self.msg.pack()
        self.msg2.pack()
        self.link.pack()
        self.protocol("WM_DELETE_WINDOW", self.exit)

        sw = min([self.root.winfo_x() + self.root.winfo_width() / 2 - 150, self.root.winfo_screenwidth() - 300])
        sw = max([0, sw])
        sh = min([self.root.winfo_y() + self.root.winfo_height() / 2 - 50, self.root.winfo_screenheight() - 150])
        sh = max([0, sh])
        print(self.root.winfo_width())
        self.geometry('300x100+%d+%d' % (sw, sh))

    def exit(self, event=None):
        self.root.focus_set()
        self.destroy()
