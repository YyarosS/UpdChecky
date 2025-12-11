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

    def get_latest_version(self, list_command, sync_command = None ):
        try:
            if(sync_command == None):
                call_version_list = subprocess.run(
                    list_command,
                    capture_output=True,
                    check=False, text=True,
                    env=os.environ)
                parsed_versions = call_version_list.stdout
                versions_commands = subprocess.run(
                    ["awk", "{print $1, $4}"],
                    text=True,
                    capture_output = True,
                    input=parsed_versions)
                parsed_commands = self.parse_output(versions_commands.stdout)
                return parsed_commands
            else:
                sync_command = subprocess.run(
                    sync_command,
                    check=True,
                    text=True,
                    stderr=subprocess.DEVNULL)
                call_version_list = subprocess.run(
                    list_command,
                    shell = True,
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
        except Exception as e:
            print("Ошибка нахождения новых версий.")
    
    def select_utility_commands(self, managers):
        utility_commands = []
        try:
            for manager in managers:
                if (managers.get(manager) == "pacman"):
                    manager_command = ["pacman", "-Q"]
                    out_latest_list = ["checkupdates"]
                    commands = [manager_command, out_latest_list]
                    utility_commands.append(commands) 
                elif(managers.get(manager) == "apt"):
                    manager_command = ["dpkg", "-l"]
                    sync_command = ["sudo", "apt", "update"]
                    out_latest_list = ["apt", "list", "--upgradable"]
                    commands = [manager_command, sync_command, out_latest_list]
                    utility_commands.append(commands) 
                elif(managers.get(manager) == "dnf"):
                    manager_command = ["dnf", "list", "installed"]
                    sync_command = ["dnf", "makecache"]
                    out_latest_list = ["dnf", "check-update"]
                    commands = [manager_command, sync_command, out_latest_list]
                    utility_commands.append(commands) 
                elif(managers.get(manager) == "Flatpak"):
                    manager_command = ["flatpak", "list",]
                    out_latest_list = ["flatpak", "remote-ls", "--updates"]
                    commands = [manager_command, out_latest_list]
                    utility_commands.append(commands)
            
            return utility_commands
        except Exception as e:
            print("Ошибка определения команд утилиты")