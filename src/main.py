from Gui import Welcome_Window, Main_Windows
from Manager import Manager as app_manager

import os

def create_welcome_screen():
    welcome_windows = Welcome_Window()
    welcome_windows.mainloop()

def load_main_window():
    if __name__ == "__main__":
        main_window = Main_Windows()

        managers = create_managers()
        utility_commands = set_utility_comands()
        #manager = app_manager()
        #utility_commands = manager.select_utility_commands()
        def set_utility_comands():
            commands = []
            for manager in  managers:
                commands.append(manager.select_utility_commands())
            return commands

        def create_managers(manager_list):
            managers = []
            for manager_name in manager_list:
                manager = app_manager(manager_list.get(manager_name))
                managers[manager_name] = manager
            return managers
        
        def is_new_version(actual):
            if actual and isinstance(actual, dict):
                return True
            return False

        def show_updated_apps(latest, current):
            parsed_latest = manager.parse_output(latest)
            if parsed_latest != None:
                apps_count = 0
                for app in parsed_latest:
                    print(f"{app} {parsed_latest.get(app)}")
                    main_window.out_app(
                        app, 
                        parsed_latest.get(app),
                        current.get(app),
                        apps_count) 
                    apps_count += 1
            else:
                print("Обновлений пока не обнаружено")
        
        current_versions = manager.get_current_version(utility_commands[0])
        lattest_versions = manager.get_latest_version(utility_commands[2], utility_commands[1],)
        update = is_new_version(current_versions, lattest_versions)

        if (update):
            show_updated_apps(lattest_versions, current_versions)
    main_window.mainloop()

data_path = "data"
file_name = "sources.json"
sources_list = os.path.join(data_path, file_name)

if (os.path.exists(sources_list)):
    load_main_window()
else:
    create_welcome_screen()
    load_main_window()