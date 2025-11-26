from Gui import *
from PacmanManager import PacmanManager as app_manager

import os
window_resolution = "800x600"

#main_windows = SourceList_Menu(window_resolution)
#main_windows.mainloop()

pacman = app_manager()
installed_apps = pacman.get_installed_packages()

project_directory = os.getcwd()
versions_directory = os.path.join(project_directory, "data")
current_version_file = os.path.join(versions_directory, "current_version.json")
if not os.path.exists(current_version_file):
    pacman.write_data_on_json(installed_apps, current_version_file)
pacman.get_current_version()