import tkinter as tk

from TriggerReporter.GU.project_managers import ProjectDisplayManager


class MainNavbar(tk.Menu):
    def __init__(self, controller, *args, **kwargs):
        tk.Menu.__init__(self, controller, *args, **kwargs)
        self.controller = controller
        # file Menu
        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label='New Project', command=self.new_project)
        self.file_menu.add_command(label='Open', command=self.open_project)
        self.file_menu.add_command(label='Save As', command=self.save_as_project, state='disabled')
        self.file_menu.add_command(label='Save', command=self.save_project, state='disabled')
        self.file_menu.add_command(label="Exit", command=self.controller.exit)

        # import menu
        self.import_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Import', menu=self.import_menu)
        self.import_menu.add_command(label='Import Monitoring Points', command=self.controller.import_monitoring_points, state='disabled')
        self.import_menu.add_command(label='Import Measurements', command=self.controller.import_measurements, state='disabled')

    def new_project(self):
        """Create a new project"""
        self.controller.project = ProjectDisplayManager.new_project()

    def open_project(self):
        """Load an existing project"""
        project = ProjectDisplayManager.open_project()
        if not project:
            # failed to pickle file so raise error
            tk.messagebox.showerror(title='Project Error',
                message='Project Failed to Load')
        else:
            self.controller.project = project
            self.controller.load_survey_window() 

    def save_project(self):
        """Saves an existing project"""
        ProjectDisplayManager.save_project(self.controller.project)
    
    def save_as_project(self):
        """Saves as an exisiting project and sets the 
        project title"""
        ProjectDisplayManager.save_as_project(self.controller.project)
        self.controller.set_project_title()

    def enable_project_menu(self):
        """If project is loaded, enables project related menu items"""
        self.file_menu.entryconfig('Save As', state='normal')
        self.file_menu.entryconfig('Save', state='normal')
        self.import_menu.entryconfig('Import Monitoring Points', state='normal')
        self.import_menu.entryconfig('Import Measurements', state='normal')
    