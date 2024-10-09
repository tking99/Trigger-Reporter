from datetime import datetime
import tkinter as tk 
from tkinter import ttk 

class AboutDisplay(tk.Toplevel):
    VERSION = 'V1.3'
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.title('About Trigger Reporter') 
        self.geometry('200x250')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        about_frame = ttk.Frame(self)
        about_frame.grid(column=0, row=0)
        about_frame.columnconfigure(0, weight=1)
        about_frame.rowconfigure(0, weight=1)

        title_style = ttk.Style()
        title_style.configure('Title.TLabel', font=('Sans', '12'))
        ttk.Label(about_frame, text='Trigger Reporter', style='Title.TLabel').grid(column=0, row=0, sticky='N')
        ttk.Label(about_frame, text=self.VERSION, style='Title.TLabel').grid(column=0, row=1, sticky='N')
        
        software_info = ttk.Frame(self)
        software_info.grid(column=0, row=1)
        ttk.Label(software_info, text='Build Date: ').grid(column=0, row=0, sticky='E')
        ttk.Label(software_info, text='Version: ').grid(column=0, row=1, sticky='E')

        ttk.Label(software_info, text='Feb 01 2024').grid(column=1, row=0, sticky='W')
        ttk.Label(software_info, text=self.VERSION).grid(column=1, row=1, sticky='W')
        ttk.Label(software_info, text=f'Copyright {datetime.now().year}, Tom King').grid(
            column=0, row=2, columnspan=2, sticky='EW', pady=10)
       
