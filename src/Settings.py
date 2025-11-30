from PackageManager import PackageManager as pm
import subprocess

class Settings:
    def __init__(self):
        self.selected_source_list = []

    def add_source(self,source_name):
        if (source_name == "From the package manager"):
            self.__determine_manager()
            #self.selected_source_list.append(source_name)
        elif (source_name == "Flatpak"):
            if (self.__check_flatpak()):
                self.selected_source_list.append(source_name)
        elif (source_name == "Snap"):
            self.__check_snap()
        print(self.selected_source_list)
        
    def __check_flatpak():
        existing_calling = subprocess.run(
            ["flatpak", "--vesion"],
            check=True,
            text=True,)
        answer =  existing_calling.stdout
        parsed_answer= pm.parse_output(answer)
        print(parsed_answer)
        # if (parsed_answer != ):
        #     return True
        # return False
    def __check_snap():
        pass
    def __determine_manager():
        pass
    def print_source_list(self):
        for source in self.selected_sources_list:
            print(source)