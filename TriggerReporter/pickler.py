import os
import pickle 


class ProjectPickler:
    @classmethod     
    def dump_project(cls, project):
        with open(project.project_path, 'wb') as f:
            pickle.dump(project, f)

    @classmethod
    def load_project(cls, project_path):
        """Checks if pickle is empty before attempting 
        to load, if empty returns None"""
        try:
            with open(project_path, 'rb') as f: 
                project = pickle.load(f)
                return project
        except:
            return


