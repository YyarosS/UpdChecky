from PackageManager import PackageManager as pm

import shutil
import os

class Settings:
    def __init__(self):
        self.__selected_sources = {}

    def add_source(self,source_name):
        self.__determine_manager(source_name)
        self.print_source_list()
        project_path = os.getcwd()
        data_path = os.path.join(project_path, "data")
        source_path=os.path.join(data_path, "sources.json")
        self.save_on_storage(file_path=source_path)

    def __determine_manager(self, manager):
        if (manager == "From the package manager"):
            manager_list= ['apt', 'dnf', 'pacman']
            dict_len = len(self.__selected_sources)
            for manager in manager_list:
                if shutil.which(manager):
                    self.__selected_sources[dict_len+1] = manager
        elif shutil.which(manager):
            self.__selected_sources[dict_len+1] = manager

    def print_source_list(self):
        for source in self.__selected_sources:
            print(source)

    def save_on_storage(self, file_path):
        pm.write_data_on_json(data=self.__selected_sources, file_name=file_path)