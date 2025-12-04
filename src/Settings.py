from PackageManager import PackageManager as pm

import shutil
import os

class Settings:
    def __init__(self):
        self.__selected_sources = {}
        self.utility_commands = []

    def add_source(self,source_name):
        self.__determine_manager(source_name)
        #self.print_source_list()
        project_path = os.getcwd()
        data_path = os.path.join(project_path, "data")
        source_path=os.path.join(data_path, "sources.json")
        self.__save_on_storage(file_path=source_path)

    def __determine_manager(self, manager):
        if (manager == "From the package manager"):
            manager_list= ['apt', 'dnf', 'pacman']
            for manager in manager_list:
                if shutil.which(manager):
                    next_key = len(self.__selected_sources)+1
                    self.__selected_sources[next_key] = manager
        elif shutil.which(manager):
            next_key = len(self.__selected_sources)+1
            self.__selected_sources[next_key] = manager

    def __save_on_storage(self, file_path):
        pm.write_data_on_json(self.__selected_sources, file_path)

    def select_utility_commands(self):
        for i in self.__selected_sources:
            if (self.__selected_sources.get(i) == "pacman"):
                manager_command = ["pacman", "-Q"]
                sync_command = ["sudo", "pacman", "-Sy"]
                out_latest_list = ["pacman", "-Qu"]
                utility = [manager_command, sync_command, out_latest_list]
                self.utility_commands.append(utility)
            elif(self.__selected_sources.get(i) == "apt"):
                manager_command = ["dpkg", "-l"]
                sync_command = ["sudo", "apt", "update"]
                out_latest_list = ["apt", "list", "--upgradable"]
                utility = [manager_command, sync_command, out_latest_list]
                self.utility_commands.append(utility)
            elif(self.__selected_sources.get(i) == "dnf"):
                manager_command = ["dnf", "list", "installed"]
                sync_command = ["dnf", "makecache"]
                out_latest_list = ["dnf", "check-update"]
                utility = [manager_command, sync_command, out_latest_list]
                self.utility_commands.append(utility)