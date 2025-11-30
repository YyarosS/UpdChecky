class Settings:
    def __init__(self):
        self.selected_source_list

    def add_source(self,source_name):
        if (source_name == "From the package manager" or
            source_name == "Flatpak" or
            source_name == "Snap"):
            self.selected_source_lisе.append(source_name)
        print(self.selected_source_list)


    def determine_manager():
        pass
    