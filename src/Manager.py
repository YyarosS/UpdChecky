from PackageManager import PackageManager as pm

import subprocess
import os

class Manager(pm):

    def get_installed_packages(self, manager_command):
        current_version_file = os.path.join(os.getcwd(), "data/current_version.json")
        if not os.path.isfile(current_version_file):
            try:
                call_respounse = subprocess.run(
                    #["pacman", "-Q"],
                    manager_command,
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

    def get_current_version(self, command):
        installed_apps = self.get_installed_packages(command)
        try:
            if installed_apps != None:
                return installed_apps
        except Exception as ex:
            print(f"Ошибка нахождения установленных пакетов или их версий")

    def get_latest_version(self, sync_command, list_command):
        
        sync_command = subprocess.run(
            #["sudo","pacman", "-Sy"],
            sync_command,
            check=True,
            text=True,
            stderr=subprocess.DEVNULL)
        versions_output = sync_command.stdout
        call_version_list = subprocess.run(
            #["pacman", "-Qu"],
            list_command,
            input=versions_output,
            capture_output=True,
            check=True, text=True)
        parsed_vesions_command = subprocess.run(["awk", "{print $1, $4}"], input=versions_output)
        return parsed_vesions_command 