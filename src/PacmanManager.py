from PackageManager import PackageManager as pm

import subprocess
import os

class PacmanManager(pm):

    def get_installed_packages(self):
        current_version_file = os.path.join(os.getcwd(), "data/current_version.json")
        if not os.path.isfile(current_version_file):
            try:
                call_respounse = subprocess.run(
                    ["pacman", "-Q"], 
                    capture_output=True, 
                    text=True, 
                    check=True)
                apps = call_respounse.stdout
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при выполнении команды: {e}")
        else:
            apps = self.out_data_from_json(current_version_file)  
        try:
            if apps:
                apps_data = self.parse_output(apps)
                return apps_data
        except Exception as ex:
            print("нет данных для обработки.")

    def get_current_version(self):
        current_verssions_file = os.path.join(os.getcwd(), "data/current_version.json")
        try:
            app = self.out_data_from_json(current_verssions_file)
            if app != None:
                for version in app.values():
                    return version
        except Exception as ex:
            print(f"объект app пуст")

    def get_latest_version(self, package_name):
        pass