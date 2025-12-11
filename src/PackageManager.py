from abc import ABC, abstractmethod

import json
import sys
import re
import os

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
        try:
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
        except Exception as e:
            print("Ошибка обработки команды.")
    
    @staticmethod
    def write_data_on_json(data, file_name):
        try:
            with open (file_name, 'w', encoding='utf-8') as base:
                json.dump(data, base, ensure_ascii= False, indent=4)
        except Exception as e:
            print("Не удалось найти или открыть файл.")

    def out_data_from_json(self, file_directory):
        try:
            with open(file_directory, 'r', encoding='utf-8') as file:
                python_object = json.load(file)
            return python_object
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON в файле '{file_directory}': {e}")
            return None
        except FileNotFoundError:
            print(f"Ошибка: Файл '{file_directory}' не найден.")
            return None
    @staticmethod
    def get_project_path():
        try:
            if getattr(sys, 'frozen', False):
                return os.path.dirname(sys.argv[0])
            
            src_path = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(src_path)
            return project_root
        except Exception as e:
            print("Путь к проекту не найден!")