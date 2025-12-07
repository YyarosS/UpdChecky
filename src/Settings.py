from PackageManager import PackageManager as pm

import shutil
import os

class Settings:
    def __init__(self):
        self.__selected_sources = {}
        self.utility_commands = []

    def add_source(self,source_name):
        self.determine_manager(source_name)
        project_path = os.getcwd()
        data_path = os.path.join(project_path, "data")
        source_path=os.path.join(data_path, "sources.json")
        self.__save_on_storage(file_path=source_path)

    def determine_manager(self, manager_name):
        if (manager_name == "From the package manager"):
            manager_list= ['apt', 'dnf', 'pacman']
            for manager in manager_list:
                if shutil.which(manager):
                    next_key = len(self.__selected_sources)+1
                    self.__selected_sources[next_key] = manager
        elif shutil.which(manager_name):
            next_key = len(self.__selected_sources)+1
            self.__selected_sources[next_key] = manager

    def __save_on_storage(self, file_path):
        pm.write_data_on_json(self.__selected_sources, file_path)

    def get_selected_sources(self):
        return self.__selected_sources