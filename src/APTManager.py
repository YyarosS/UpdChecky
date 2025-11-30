from PackageManager import PackageManager as pm

import subprocess
import json
import os

class APTManager(pm):
    def get_installed_packages(self):
        current_version_file = os.path.join(os.getcwd(), "data/current_version.json")
        if not os.path.isfile(current_version_file):
            try:
                command_f_calling = subprocess.run(
                    ["apt", "list"],
                    apture_output=True,
                    check=True,
                    text=True)
                apps = command_f_calling.stdout
            except subprocess.CalledProcessError as ex:
                print(f"Ошибка при выполнении команды: {ex}")
        else:
            apps = self.out_data_from_json(current_version_file)
    def get_current_version(self):
        pass

    def get_latest_version(self):
        pass