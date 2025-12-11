from Gui import Welcome_Window, Main_Window
from Manager import Manager as app_manager

import os

def create_welcome_screen():
    try:
        welcome_windows = Welcome_Window()
        welcome_windows.mainloop()
    except Exception as e:
        print("Ошибка создания приветственного окна!")

def load_main_window():
    if __name__ == "__main__":
        try:
            main_window = Main_Window()
        
            manager = app_manager()
            sources = get_sources(manager) 
            utility_commands = manager.select_utility_commands(sources)
        except Exception as e:
            print("Ошибка открытия программы!")

        all_updates = {}
        cur_versions = {}
        try:
            for utility in utility_commands:
                if (len(utility) == 3):
                    current_versions = manager.get_current_version(utility[0])
                    latest_versions = manager.get_latest_version(utility[2], utility[1])
                    all_updates.update(latest_versions)
                    cur_versions.update(current_versions)
                else:
                    current_versions = manager.get_current_version(utility[0])
                    latest_versions = manager.get_latest_version(utility[1])
                    all_updates.update(latest_versions)
                    cur_versions.update(current_versions)
        except Exception as e:
            print("Ошибка определения версий программ!")

        update = is_new_version(all_updates)

        if (update):
            show_updated_apps(all_updates, cur_versions, main_window)
        else:
            main_window.empty_out()

        main_window.mainloop()
def get_sources(manager):
    try:
        data_path = "data"
        file_name = "sources.json"
        sources_path = os.path.join(data_path, file_name)
        sources = manager.out_data_from_json(sources_path)
        return sources
    except Exception as e:
        print("Источники не были найдены!")

def is_new_version(actual):
    if actual:
        return True
    return False

def show_updated_apps(latest_versions,current_versions, main_window):
    for app in latest_versions:
        main_window.out_apps(app, current_versions.get(app), latest_versions.get(app))

data_path = "data"
file_name = "sources.json"
sources_list = os.path.join(data_path, file_name)

if (os.path.exists(sources_list)):
    load_main_window()
else:
    create_welcome_screen()
    load_main_window()