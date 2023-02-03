from functools import partial

from datetime import datetime

import tkinter as tk 
from tkinter import ttk
from tkinter import tix 

from tkcalendar import Calendar, DateEntry
from tktimepicker import SpinTimePickerModern, constants

from TriggerReporter.models import MonitoringTypes, ReportVar, ArrayVar
from TriggerReporter.Matplot.tables import RadialMonitoringResultsTable, ConvergenceMonitoringResultsTable
from TriggerReporter.processors import ReportDataProcessor
from TriggerReporter.factories import MonitoringResultsTableFactory

class SurveyMainDisplay(ttk.Frame):
    def __init__(self, container, project, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.project = project
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.vars = {}
        self.today_date_time = datetime.now()
        self.array_canvas = ArrayCanvas(self)
        self.array_canvas.grid(column=0, row=0, sticky='NSEW')
  
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.grid(column=0, row=1, padx=10, pady=10, sticky='NSEW')
        self.bottom_frame.columnconfigure(0, weight=1)
        ttk.Separator(self.bottom_frame, orient=tk.HORIZONTAL).grid(column=0, row=0, columnspan=10, sticky='ew')
           
        self.button_frame = ttk.Frame(self.bottom_frame)
        self.button_frame.grid(column=1, row=1, sticky='NW', padx=10, pady=10)
        ttk.Button(self.button_frame, text='Print Reports', command=self.print_reports, padding=(10,5)).grid(
            column=0, row=0, padx=5, pady=5, sticky='NE')

    def print_reports(self):
        if self.vars:
            report_data_processor = ReportDataProcessor(self.vars)
            report_datas = report_data_processor.process_report_data()
            processed_report_data = []
            for report_data in report_datas:
                table = MonitoringResultsTableFactory.get_monitoring_table(report_data.mt_type)
                if table:
                    processed_report_data.append(report_data)
                    table(report_data)
            
            if processed_report_data:
                self.print_report_success(processed_report_data)
            else:
                self.print_report_unsuccess()

    
    def print_report_success(self, processed_report_data):     
        tk.messagebox.showinfo(
            title='Successfully Printed Reports')

    def print_report_unsuccess(self):
        tk.messagebox.showerror(title='Unsuccessfully Printed reports', 
            message='No reports were printed')


class ArrayCanvas(tk.Canvas):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.array_frame = ttk.Frame(container)
        self.array_frame.grid(column=0, row=0)
        self.scrollable_window = self.create_window((0, 0), window=self.array_frame,
            anchor="nw")

        self.bind("<Configure>", self._configure_window_size)
        self.array_frame.bind("<Configure>", self._configure_scroll_region)
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)

        self.load_array()

    def _configure_scroll_region(self, event):
            self.configure(scrollregion=self.bbox("all"))

    def _configure_window_size(self, event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

    def _on_mousewheel(self, event):
        self.yview_scroll(-int(event.delta/120), "units")

    def load_array(self):
        count = -1 
        for site in self.container.project.sites:
            count += 1
            ttk.Label(self.array_frame, text=site.name.title()).grid(column=0, row=count, sticky='NW', padx=3, pady=6)
            count +=1
            ttk.Separator(self.array_frame, orient=tk.HORIZONTAL).grid(column=0, row=count, columnspan=2, sticky='ew')
            for heading in site.headings:
                report_var = ReportVar(heading)
                self.container.vars[heading] = report_var
                count += 1 
                ttk.Label(self.array_frame, text=heading.name.title()).grid(column=1, row=count, sticky='NW', padx=10, pady=6)
                ttk.Label(self.array_frame, text=MonitoringTypes.CONVERGENCE.value).grid(column=3, row=count, sticky='NEW', padx=3, pady=3,
                    columnspan=2)
                ttk.Label(self.array_frame, text=MonitoringTypes.DIVERGENCE.value).grid(column=5, row=count, sticky='NEW', padx=3, pady=3,
                    columnspan=2)
                ttk.Label(self.array_frame, text=MonitoringTypes.RADIAL.value[0:6]).grid(column=7, row=count, sticky='NEW', padx=3, pady=3,
                    columnspan=2) 
                ttk.Label(self.array_frame, text='Surveyor: ').grid(column=9, row=count, sticky='NW', padx=3, pady=3)
                ttk.Entry(self.array_frame, textvariable=report_var.surveyor).grid(column=10, row=count, sticky='NW', padx=5, pady=3)
                count +=1
                ttk.Separator(self.array_frame, orient=tk.HORIZONTAL).grid(column=1, row=count, columnspan=10, sticky='ew')
                for array in heading.arrays:
                    array.update_active()
                    array_var = ArrayVar(array)
                    report_var.array_vars[array] = array_var 
                    count +=1 
                    ttk.Button(self.array_frame, text='Edit').grid(column=1, row=count, sticky='NW', padx=3, pady=3)
                    ttk.Label(self.array_frame, text=array.name.title()).grid(column=2, row=count, sticky='NW', padx=3, pady=3)

                   ### Convergence
                    ttk.Checkbutton(self.array_frame, variable=array_var.vars[MonitoringTypes.CONVERGENCE.value][0], onvalue=True,
            offvalue=False, command=partial(self.toggle_array, array, MonitoringTypes.CONVERGENCE.value)).grid(column=3, row=count, sticky='NW', padx=3, pady=3)
                    menu_con = tk.OptionMenu(self.array_frame, array_var.vars[MonitoringTypes.CONVERGENCE.value][1], 
                    array.get_latest_date(MonitoringTypes.CONVERGENCE.value), *array.get_monitoring_dates(MonitoringTypes.CONVERGENCE.value))
                    menu_con.grid(column=4, row=count, sticky='NW')
                   
                    ### Divergence 
                    ttk.Checkbutton(self.array_frame, variable=array_var.vars[MonitoringTypes.DIVERGENCE.value][0], onvalue=True,
            offvalue=False, command=partial(self.toggle_array, array, MonitoringTypes.DIVERGENCE.value)).grid(column=5, row=count, sticky='NW', padx=3, pady=3)
                    menu_con = tk.OptionMenu(self.array_frame, array_var.vars[MonitoringTypes.DIVERGENCE.value][1],
                    array.get_latest_date(MonitoringTypes.DIVERGENCE.value), *array.get_monitoring_dates(MonitoringTypes.DIVERGENCE.value))
                    menu_con.grid(column=6, row=count, sticky='NW')
                     
                    ### Radial
                    ttk.Checkbutton(self.array_frame, variable=array_var.vars[MonitoringTypes.RADIAL.value][0], onvalue=True,
            offvalue=False, command=partial(self.toggle_array, array, MonitoringTypes.RADIAL.value)).grid(column=7, row=count, sticky='NW', padx=3, pady=3)
                    menu_con = tk.OptionMenu(self.array_frame, array_var.vars[MonitoringTypes.RADIAL.value][1], array.get_latest_date(MonitoringTypes.RADIAL.value), *array.get_monitoring_dates(MonitoringTypes.RADIAL.value))
                    menu_con.grid(column=8, row=count, sticky='NW')
                 
    def toggle_array(self, array, mt_type):
        arr = array.get_array(mt_type)
        report_var = self.container.vars[array.heading]
        array_vars = report_var.array_vars[array]    
        if arr is not None:
            arr.toggle_active()
            array_vars.vars[mt_type][0].set(arr.active) 
        else:
            array_vars.vars[mt_type][0].set(False)

