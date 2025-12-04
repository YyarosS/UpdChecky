from abc import ABC, abstractmethod

import json
import os
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
        
    def write_data_on_json(data, file_name):
        with open (file_name, 'w', encoding='utf-8') as base:
            json.dump(data, base, ensure_ascii= False, indent=4)

    def out_data_from_json(self, file_directory):
        try:
            with open(file_directory, 'r', encoding='utf-8') as file:
                python_object = json.load(file)
                #for package_name, package_version in python_object.items():
                    #print(f"{package_name} {package_version}") 
            return python_object
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON в файле '{file_directory}': {e}")
            return None
        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_directory}' не найден.")
            return None
        
    def add_installed_source(self, file_path, new_source, list_key = "installation_sources"):
        data = {}
        
        if list_key not in data or not isinstance(data.get(list_key), list):
            data[list_key] = []
            
        if isinstance(data[list_key], list):
            data[list_key].append(new_source)
        else:
            print(f"Ошибка: Значение по ключу '{list_key}' не является списком.")
            return False
        
        try:
            self.write_data_on_json(data=data, file_name=file_path)
            print(f"Успех: Источник '{new_source.get('manager', 'Новый источник')}' добавлен в файл '{file_path}'.")
            return True
        except IOError as e:
            print(f"Ошибка записи файла '{file_path}': {e}")
            return False