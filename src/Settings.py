from PackageManager import PackageManager as pm

import subprocess
import os

class Settings:
    def __init__(self):
        self.__selected_sources = {}

    def add_source(self,source_name):
        try:
            self.__determine_manager(source_name)
            project_path = pm.get_project_path()
            data_path = os.path.join(project_path, "data")
            source_path=os.path.join(data_path, "sources.json")
            self.__save_on_storage(source_path)
        except Exception as e:
            print("Ошибка добавления источника пакетов!")

    def __determine_manager(self, manager):
        try:
            if(manager == "From the package manager"):
                managers= ["apt", "dnf", "pacman"]
                for manager_name in managers:
                    try:
                        subprocess.run(
                        [manager_name, '--version'], 
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
                        key = len(self.__selected_sources)+1
                        self.__selected_sources[key] = manager_name
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print("Ошибка, источник не был найден!")
            else:
                try:
                    subprocess.run(
                        [manager.lower(), '--version'], 
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
                    key = len(self.__selected_sources)+1
                    self.__selected_sources[key] = manager
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("Ошибка, источник не был найден!")
        except Exception as e:
            print("Ошибка определения менеджера пакетов!")
    def __save_on_storage(self, file_path):
        pm.write_data_on_json(self.__selected_sources, file_path)