from PackageManager import PackageManager as pm

import subprocess
import os

class Manager(pm):

    def get_installed_packages(self, manager_command):
        try:
            call_respounse = subprocess.run(
                    manager_command,
                    capture_output=True, 
                    text=True, 
                    check=True)
            apps = call_respounse.stdout

            if apps:
                apps_data = self.parse_output(apps)
                return apps_data
        except subprocess.CalledProcessError as e:
                print(f"Ошибка при выполнении команды: {e}")  
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
            sync_command,
            check=True,
            text=True,
            stderr=subprocess.DEVNULL)
        call_version_list = subprocess.run(
            list_command,
            capture_output=True,
            check=True, text=True)
        parsed_versions = call_version_list.stdout
        versions_commands = subprocess.run(
            ["awk", "{print $1, $4}"],
            text=True,
            capture_output = True,
            input=parsed_versions)
        parsed_commands = self.parse_output(versions_commands.stdout)
        return parsed_commands
    
    def select_utility_commands(self, managers):
        for manager in managers:
            if (managers.get(manager) == "pacman"):
                manager_command = ["pacman", "-Q"]
                sync_command = ["sudo", "pacman", "-Sy"]
                out_latest_list = ["pacman", "-Qu"]
                return [manager_command, sync_command, out_latest_list]
            elif(managers.get(manager) == "apt"):
                manager_command = ["dpkg", "-l"]
                sync_command = ["sudo", "apt", "update"]
                out_latest_list = ["apt", "list", "--upgradable"]
                return [manager_command, sync_command, out_latest_list]
            elif(managers.get(manager) == "dnf"):
                manager_command = ["dnf", "list", "installed"]
                sync_command = ["dnf", "makecache"]
                out_latest_list = ["dnf", "check-update"]
                return [manager_command, sync_command, out_latest_list]
            # elif(manager == "Flatpak"):
            #     manager_command = ["dnf", "list", "installed"]
            #     sync_command = ["dnf", "makecache"]
            #     out_latest_list = ["dnf", "check-update"]
            #     return [manager_command, sync_command, out_latest_list]