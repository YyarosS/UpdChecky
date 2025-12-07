from PackageManager import PackageManager as pm
from Settings import Settings as set
import subprocess
import os

class Manager(pm):
    def __init__(self, manager_name):
        super().__init__()
        self.manager_name = self.set_manager_name(manager_name)
        # settings = set()
        # sources = settings.get_selected_source
    
    def set_manager_name(self,  manager_name):
        sources = self.get_sources()
        for source in sources:
            if(manager_name == sources.get(source)):
                return manager_name
            
    def get_sources(self):
        data_path = os.path.join(os.getcwd(), "data")
        sources_path = os.path.join(data_path,"sources.json")
        sources = self.out_data_from_json(sources_path)
        return sources
    
    def get_installed_packages(self, manager_command):
        try:
            call_respounse = subprocess.run(
                manager_command,
                capture_output=True, 
                text=True, 
                check=True)
            apps = call_respounse.stdout
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

    def get_latest_version(self, list_command , sync_command = None):
        # settings = set()
        # settings.determine_manager()
        # sources = settings.get_selected_sources
        # self.out_data_from_json()
        # keys_count = sources.keys()
        
 
        if (self.manager_name != "Flatpak" and self.manager_name != "Snap"):
            sync_command = subprocess.run(
                sync_command,
                check=True,
                text=True,
                stderr=subprocess.DEVNULL)
                # versions_output = sync_command.stdout
                # call_version_list = subprocess.run(
                #     list_command,
                #     # input=versions_output,
                #     capture_output=True,
                #     check=True, text=True)
                # call_out_list = call_version_list.stdout
                # parsed_vesions_command = subprocess.run(
                #     ["awk", "{print $1, $4}"],
                #     input=call_out_list,
                #     capture_output=True,
                #     text=True).stdout
                # return parsed_vesions_command
        call_version_list = subprocess.run(
            list_command,
                    #input=versions_output,
            capture_output=True,
            check=True, text=True)
        call_out_list = call_version_list.stdout
        parsed_vesions_command = subprocess.run(
                    ["awk", "{print $1, $4}"],
                    input=call_out_list,
                    capture_output=True,
                    text=True).stdout
        return parsed_vesions_command
    
    def select_utility_commands(self):
        sources = self.get_sources()
        for i in sources:
            if (sources.get(i) == "pacman"):
                manager_command = ["pacman", "-Q"]
                sync_command = ["sudo", "pacman", "-Sy"]
                out_latest_list = ["pacman", "-Qu"]
                utility = [manager_command, sync_command, out_latest_list]
                return utility
            elif(sources.get(i) == "apt"):
                manager_command = ["dpkg", "-l"]
                sync_command = ["sudo", "apt", "update"]
                out_latest_list = ["apt", "list", "--upgradable"]
                utility = [manager_command, sync_command, out_latest_list]
                return utility
            elif(sources.get(i) == "dnf"):
                manager_command = ["dnf", "list", "installed"]
                sync_command = ["dnf", "makecache"]
                out_latest_list = ["dnf", "check-update"]
                utility = [manager_command, sync_command, out_latest_list]
                return utility
            elif (sources.get(i) == "Flatpak"):
                manager_command = ["flatpak", "list"]
                out_latest_list = ["flatpak", "-n"]
                utility = [manager_command, out_latest_list]
                return utility
            elif (sources.get(i) == "Snap"):
                manager_command = ["snap", "list"]
                out_latest_list = ["snap", "refresh", "--list"]
                utility = [manager_command, out_latest_list]
                return utility