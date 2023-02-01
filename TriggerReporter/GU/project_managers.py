import os
import tkinter as tk 
from tkinter import ttk 
from tkinter.filedialog import asksaveasfile, askopenfile
from pathlib import Path

from TriggerReporter.models import TriggerReporterProject
from TriggerReporter.pickler import ProjectPickler

#os.path.basename(Path(project_path))

class ProjectDisplayManager:    
    @classmethod 
    def new_project(self):
        """Creates a new project"""
        project_path = asksaveasfile(filetypes=TriggerReporterProject.FILETYPE,
            defaultextension=TriggerReporterProject.FILETYPE[0][1])
        path = Path(project_path.name)
        if project_path and path.exists():
            path = Path(project_path.name)
            project = TriggerReporterProject(project_path.name, os.path.basename(path))
            # dump the project 
            ProjectPickler.dump_project(project)
            return project

    @classmethod 
    def open_project(cls):
        """Opens an existing project"""
        project_path = askopenfile(filetypes=TriggerReporterProject.FILETYPE,
            defaultextension=TriggerReporterProject.FILETYPE[0][1])
        if project_path:
            return ProjectPickler.load_project(project_path.name)

    @classmethod
    def save_project(cls, project):
        """Saves an existing project"""
        ProjectPickler.dump_project(project)

    @classmethod 
    def save_as_project(cls, project):
        """Saves as an existing project"""
        project_path = asksaveasfile(filetypes=TriggerReporterProject.FILETYPE,
            defaultextension=TriggerReporterProject.FILETYPE[0][1])
        if project_path:
            project.project_path = project_path.name
            ProjectPickler.dump_project(project)

    @classmethod 
    def import_monitoring_points(cls, project):
        return askopenfile()

    @classmethod 
    def import_measurements(cls, project):
        return askopenfile()
      


