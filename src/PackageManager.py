from abc import ABC, abstractmethod

import json
import re

class PackageManager(ABC):
    """
    Абстрактный класс. Обязывает всех наследников уметь
    находить версии программ.
    """
    @abstractmethod
    def get_installed_packages(self):
        """Возвращает список имен установленных пакетов."""
        pass

    @abstractmethod
    def get_current_version(self, package_name):
        """Находит версию, которая сейчас стоит в системе."""
        pass

    @abstractmethod
    def get_latest_version(self, package_name):
        """Находит последнюю доступную версию в репозитории."""
        pass

    def parse_output(self, terminal_output):

        package_data = {}
        package_out = terminal_output.strip().split('\n')
        pattern = re.compile(r'(.+?)\s+(.+)')

        for  package in package_out:
            package = package.strip()
            if  not package:
                continue
            match = pattern.match(package)
            if match:
                package_name = match.group(1).strip()
                package_version = match.group(2).strip()
                package_data[package_name] = package_version
        return package_data
        
    def write_data_on_json(self, data, file_name):
        with open (file_name, 'w', encoding='utf-8') as base:
            json.dump(data, base, ensure_ascii= True, indent=4)

    def out_data_from_json(self, file_directory):
        try:
            with open(file_directory, 'r', encoding='utf-8') as file:
                python_object = json.load(file)
                for package_name, package_version in python_object.items():
                    print(f"{package_name} {package_version}") 
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON в файле '{file}': {e}")
            return None
        except FileNotFoundError:
            print(f"Ошибка: Файл '{file}' не найден.")
            return None