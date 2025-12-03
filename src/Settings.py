from PackageManager import PackageManager as pm

import shutil

class Settings:

    def add_source(self,source_name):
        selected_source_list = self.__determine_managers(source_name)
        self.print_source_list()
        pm.write_data_on_json(selected_source_list, "sources_list.json")

    def __determine_managers():
        managers = ['apt', 'dnf', 'pacman', 'zypper', "flatpak", "snap"]
        installed_managers = []

        for manager in managers:
            if shutil.which(manager):
                installed_managers.append(manager)
        return installed_managers

    def print_source_list(self):
        for source in self.selected_sources_list:
            print(source)