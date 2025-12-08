from Gui import Welcome_Window, Main_Windows
from Manager import Manager as app_manager

import os

def create_welcome_screen():
    welcome_windows = Welcome_Window()
    welcome_windows.mainloop()

def load_main_window():
    if __name__ == "__main__":
        main_window = Main_Windows()
        
        manager = app_manager()

        sources = get_sources(manager) 
        utility_commands = manager.select_utility_commands(sources)
        
        # for utility in utility_commands:
        #     for commands in utility:
        current_versions = manager.get_current_version(utility_commands[0])
        latest_versions = manager.get_latest_version(utility_commands[1], utility_commands[2])

        update = is_new_version(latest_versions)

        if (update):
            show_updated_apps(latest_versions, current_versions, main_window)

        main_window.mainloop()

def get_sources(manager):
    data_path = os.path.join(os.getcwd(), "data")
    sources_path = os.path.join(data_path,"sources.json")
    sources = manager.out_data_from_json(sources_path)
    return sources

def is_new_version(actual):
    if actual != None:
        return True
    return False

def show_updated_apps(latest_versions,current_versions, main_window):
    count = 0
    for app in latest_versions:
        print(f"{app} {latest_versions.get(app)}")
        main_window.out_apps(app, current_versions, latest_versions.get(app), count)
        count +=1

data_path = "data"
file_name = "sources.json"
sources_list = os.path.join(data_path, file_name)

if (os.path.exists(sources_list)):
    load_main_window()
else:
    create_welcome_screen()
    load_main_window()