from PackageManager import PackageManager as pm

import shutil
import os

class Settings:
    def __init__(self):
        self.__selected_sources = []

    def add_source(self,source_name):
        self.__determine_manager(source_name)
        self.print_source_list()
        project_path = os.getcwd()
        data_path = os.path.join(project_path, "data")
        file_path=os.path.join(data_path, "sources.json")
        self.save_on_storage(self.__selected_sources, file_path=file_path)

    def __determine_manager(self, manager):

        if (manager == "From package manager"):
            manager_list= ['apt', 'dnf', 'pacman']
            for manager in manager_list:
                if shutil.which(manager):
                    self.__selected_sources.append(manager)
        if shutil.which(manager):
            self.__selected_source.append(manager)

    def print_source_list(self):
        for source in self.__selected_sources:
            print(source)

    def save_on_storage(self, sources, file_path):
        for source in sources:
            pm.add_installed_source(file_path=file_path, new_source=source)