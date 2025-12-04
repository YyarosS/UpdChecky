from Gui import Welcome_Window, Main_Windows
from Manager import Manager as app_manager

import os

def create_welcome_screen():
    welcome_windows = Welcome_Window()
    welcome_windows.mainloop()

def load_main_window():
    if __name__ == "__main__":
        main_window = Main_Windows()
        
        pacman = app_manager()

        def is_new_version(current, actual):
            for cur_version in current:
                for new_version in actual:
                    if (cur_version == new_version):
                        return False
                    return True
                
        def show_updated_apps():
            if lattest_versions != None:
                for app in lattest_versions:
                    print(f"{app} {lattest_versions.get(app)}")
            else:
                print("Обновлений пока не обнаружено")

        current_versions = pacman.get_current_version()
        lattest_versions = pacman.get_latest_version()

        update = is_new_version(current_versions, lattest_versions)

        if (update):
            show_updated_apps()

        main_window.mainloop()

data_path = "data"
file_name = "sources.json"
sources_list = os.path.join(data_path, file_name)

if (os.path.exists(sources_list)):
    load_main_window()
else:
    create_welcome_screen()
    load_main_window()