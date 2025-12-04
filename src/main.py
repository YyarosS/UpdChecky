from Gui import Welcome_Window, Main_Windows
from Manager import Manager as app_manager

from Settings import Settings as set
import os

def create_welcome_screen():
    welcome_windows = Welcome_Window()
    welcome_windows.mainloop()

def load_main_window():
    if __name__ == "__main__":
        main_window = Main_Windows()
        main_window.mainloop()

        settings = set()
        settings.select_utility_commands()
        utility_commands = settings.utility_commands
        manager = app_manager()

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
        
        for utility in utility_commands:
            for commands in utility:
                current_versions = manager.get_current_version(commands[0])
                lattest_versions = manager.get_latest_version(commands[1], commands[2])

        update = is_new_version(current_versions, lattest_versions)

        if (update):
            show_updated_apps()

data_path = "data"
file_name = "sources.json"
sources_list = os.path.join(data_path, file_name)

if (os.path.exists(sources_list)):
    load_main_window()
else:
    create_welcome_screen()
    load_main_window()