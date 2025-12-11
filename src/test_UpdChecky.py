import subprocess
import pytest
import json
import os

import main
from PackageManager import PackageManager
from Manager import Manager
from Settings import Settings

# --- Тесты для PackageManager (Базовые утилиты) ---

class TestPackageManager:
    
    # Тестируем, что парсинг вывода терминала работает корректно
    def test_parse_output_valid(self):
        manager = Manager()
        terminal_output = "package-name-1 1.0.1\npackage-name-2 2.5.0\n  \npackage-name-3 3.0"
        
        expected = {
            "package-name-1": "1.0.1",
            "package-name-2": "2.5.0",
            "package-name-3": "3.0"
        }
        
        result = manager.parse_output(terminal_output)
        assert result == expected

    # Тест на чтение данных из существующего JSON-файла
    def test_out_data_from_json_success(self, tmp_path):
        manager = Manager()
        test_data = {"key1": "value1", "key2": 42}
        
        temp_file = tmp_path / "test_sources.json"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f)
            
        result = manager.out_data_from_json(str(temp_file))
        assert result == test_data

    # Тест на запись данных в JSON-файл
    def test_write_data_on_json_success(self, tmp_path):
        test_data = {"manager": "apt", "id": 1}
        temp_file = tmp_path / "output.json"
        
        PackageManager.write_data_on_json(test_data, str(temp_file))
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            read_data = json.load(f)
            
        assert read_data == test_data

# --- Тесты для Settings (Сохранение источников) ---

class TestSettings:
    
    # Мокаем __determine_manager и __save_on_storage, чтобы избежать внешних вызовов и записи
    def test_add_source_calls_internals(self, mocker):
        settings = Settings()
        
        mock_determine = mocker.patch.object(settings, '_Settings__determine_manager')
        mock_save = mocker.patch.object(settings, '_Settings__save_on_storage')

        settings.add_source("Flatpak")
        
        mock_determine.assert_called_once_with("Flatpak")
        mock_save.assert_called_once()


    # Тест логики определения менеджера пакетов (имитация успешного поиска)
    def test_determine_manager_success(self, mocker):
        settings = Settings()
        
        mock_run = mocker.patch('subprocess.run')
        
        settings._Settings__determine_manager("Flatpak")
        
        expected_sources = {1: "Flatpak"}
        assert settings._Settings__selected_sources == expected_sources

        mock_run.assert_called_once()
        
    
    # Тест логики определения пакетного менеджера (имитация отсутствия менеджера)
    def test_determine_manager_not_found(self, mocker):
        settings = Settings()
        
        mock_run = mocker.patch('subprocess.run', side_effect=FileNotFoundError)
        
        settings._Settings__determine_manager("NonExistentManager")
    
        assert settings._Settings__selected_sources == {}
        # Проверяем, что subprocess.run был вызван
        mock_run.assert_called_once()


# --- Тесты для Manager (Логика команд) ---

class TestManager:
    
    # Тест для select_utility_commands
    def test_select_utility_commands(self):
        manager = Manager()
        
        # Имитируем словарь источников, как если бы он был прочитан из sources.json
        mock_managers = {
            "1": "pacman",
            "2": "apt",
            "3": "Flatpak",
            "4": "dnf"
        }
        
        result = manager.select_utility_commands(mock_managers)
        
        # Проверяем, что результат содержит корректные списки команд
        expected_pacman = [["pacman", "-Q"], ["checkupdates"]]
        expected_apt = [["dpkg", "-l"], ["sudo", "apt", "update"], ["apt", "list", "--upgradable"]]
        expected_dnf = [["dnf", "list", "installed"], ["dnf", "makecache"], ["dnf", "check-update"]]
        expected_flatpak = [["flatpak", "list"], ["flatpak", "remote-ls", "--updates"]]

        assert expected_pacman in result
        assert expected_apt in result
        assert expected_dnf in result
        assert expected_flatpak in result
        assert len(result) == 4
        
    # Тест для get_installed_packages (имитация успешного выполнения)
    def test_get_installed_packages_success(self, mocker):
        manager = Manager()
        
        # 1. Имитируем успешный вывод subprocess.run
        mock_run_result = mocker.MagicMock()
        mock_run_result.stdout = "app1 1.0\napp2 2.5"
        
        # 2. Мокаем subprocess.run для возврата нашего объекта-результата
        mocker.patch('subprocess.run', return_value=mock_run_result)
        
        # 3. Вызываем тестируемый метод
        result = manager.get_installed_packages(["some", "command"])
        
        # 4. Проверяем результат
        assert result == {"app1": "1.0", "app2": "2.5"}

# --- Тесты для main.py (Вспомогательные функции) ---

class TestMainFunctions:

    # Тест для get_sources (имитация успешного чтения файла)
    def test_get_sources_success(self, mocker, tmp_path):
        mock_manager = mocker.MagicMock(spec=Manager)
        
        expected_sources = {"1": "apt", "2": "Flatpak"}
        mock_manager.out_data_from_json.return_value = expected_sources
        
        mocker.patch('os.getcwd', return_value=str(tmp_path))
        
        result = main.get_sources(mock_manager)
        
        expected_path = os.path.join(str(tmp_path), "data", "sources.json")
        mock_manager.out_data_from_json.assert_called_once_with(expected_path)
        
        assert result == expected_sources
        
    def test_is_new_version(self):
        assert main.is_new_version({"app1": "2.0"}) is True
        assert main.is_new_version({}) is False
        assert main.is_new_version(None) is False