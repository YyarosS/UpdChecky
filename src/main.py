from Gui import SourceList_Menu
#from Manager import Manager as app_manager

import os

main_windows = SourceList_Menu()
main_windows.mainloop()

# pacman = app_manager()
# installed_apps = pacman.get_installed_packages()

# def cached_versions_file():
#     project_directory = os.getcwd()
#     versions_directory = os.path.join(project_directory, "data")
#     current_version_file = os.path.join(versions_directory, "current_version.json")
#     return current_version_file

# def is_new_version(current, actual):
#     for cur_version in current:
#         for new_version in actual:
#             if cur_version == new_version:
#                 return False
#             return True
        
# def show_updated_apps():
#     if lattest_versions != '':
#         print(lattest_versions)
#     else:
#         print("Обновлений пока не обнаружено")

# app_varsions = cached_versions_file()

# if not os.path.exists(app_varsions):
#     pacman.write_data_on_json(installed_apps, app_varsions)

# current_versions =pacman.get_current_version()
# lattest_versions = pacman.get_latest_version()

# update = is_new_version(current_versions, lattest_versions)

# if update:
#     show_updated_apps()