import os
import time
from datetime import datetime 
from sys import exit 
from pathlib import Path

import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox

from TriggerReporter.GU.navigation import MainNavbar
from TriggerReporter.GU.project_managers import ProjectDisplayManager
from TriggerReporter.GU.report_displays import SurveyMainDisplay
from TriggerReporter.processors import MonitoringPointProcessor, MeasurementPointProcessor
from TriggerReporter.readers import CSVFileReader


from TriggerReporter.Matplot.tables import ConvergenceMonitoringResultsTable, DivergenceMonitoringResultsTable


class TriggerReporter(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title('Trigger Reporter')
        self.main_frame = ttk.Frame(self, style='Main.TFrame')
        self.main_frame.grid(column=0, row=0, padx=5, pady=5, sticky='NESW')
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self._project = None
        self.nav_menu = MainNavbar(self, tearoff=0)
        self.config(menu=self.nav_menu)
        self.survey_display = None
    
    @property 
    def project(self):
        return self._project 

    @project.setter 
    def project(self, project):
        if project: 
            self._project = project 
            self.title(f'Trigger Reporter - {self.project.name}')
            self.open_project()

    def load_survey_window(self):
        if self._project:
            if self.survey_display:
                self.survey_display.forget()
                self.survey_display.destroy()
            self.survey_display = SurveyMainDisplay(self.main_frame, self._project)
            self.survey_display.grid(column=0, row=0, sticky='NSEW')

              
    def open_project(self):
        self.nav_menu.enable_project_menu()

    def import_monitoring_points(self):
        mon_files = ProjectDisplayManager.import_monitoring_points(self.project)
        if mon_files:
            mon_processor = MonitoringPointProcessor(self.project)
            for mon_file in mon_files:
                lines = CSVFileReader.read(Path(mon_file), False)
                mon_processor.process_mass_monitoring_points(lines)
            self.load_survey_window()
    
    def import_measurements(self):
        meas_files = ProjectDisplayManager.import_measurements(self.project)
        if meas_files:
            meas_processor = MeasurementPointProcessor(self.project)
            for meas_file in meas_files:
                lines = CSVFileReader.read(Path(meas_file), True)
                meas_processor.process_measurement_points(lines)
            self.load_survey_window()
            
    def set_project_title(self):
        """Appends the project name to the title"""
        self.title(f'Trigger Reporter - {self.project.name}')
    
    def exit(self):
        """Asks if user wants to save before 
        exiting out of the program"""
        if self._project:
            answer = messagebox.askyesnocancel(
                title='Quit', message='Do you wish to save before quitting?')  
            if answer is None:
                # user cancels
                return
            elif answer:
                self.nav_menu.save_as_project()
        exit()
     
end_trial = datetime.strptime('31-03-2023', '%d-%m-%Y')

if __name__ == "__main__":
    if datetime.today() < end_trial:
        main = TriggerReporter()
        main.protocol('WM_DELETE_WINDOW', main.exit)
        main.mainloop()
    else:
        tk.messagebox.showerror(title='Version Error',
            message='Please contact Tom King for latest version.')

