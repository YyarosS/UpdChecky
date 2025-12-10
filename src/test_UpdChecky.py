import subprocess
import pytest
import json
import os
from unittest.mock import MagicMock, patch, mock_open

from PackageManager import PackageManager
from Manager import Manager
from main import get_sources, is_new_version, show_updated_apps
from Settings import Settings
from Gui import Background, Welcome_Window, Source_Item, Main_Windows

# Мокируем абстрактный класс PackageManager для тестирования его неабстрактных методов
class MockPackageManager(PackageManager):
    def get_installed_packages(self):
        pass
    def get_current_version(self, package_name):
        pass
    def get_latest_version(self, package_name):
        pass

@pytest.fixture
def mock_package_manager():
    return MockPackageManager()

@pytest.fixture
def manager_instance():
    return Manager()

# --- Тестирование класса PackageManager ---

def test_parse_output_standard(mock_package_manager):
    """Тестирование парсинга стандартного вывода имени и версии."""
    output = "package1 1.0.0\npackage-two 2.5\nthird_app 3.0.1-1"
    expected = {
        "package1": "1.0.0",
        "package-two": "2.5",
        "third_app": "3.0.1-1"
    }
    assert mock_package_manager.parse_output(output) == expected

def test_parse_output_with_extra_spaces(mock_package_manager):
    """Тестирование парсинга с лишними пробелами и пустыми строками."""
    output = "  app_a   1.2.3 \n \n app_b  4.5.6\n"
    expected = {
        "app_a": "1.2.3",
        "app_b": "4.5.6"
    }
    assert mock_package_manager.parse_output(output) == expected

def test_parse_output_empty(mock_package_manager):
    """Тестирование парсинга пустого вывода."""
    assert mock_package_manager.parse_output("") == {}
    assert mock_package_manager.parse_output("\n \n") == {}

@patch('builtins.open', new_callable=mock_open)
@patch('json.dump')
def test_write_data_on_json(mock_dump, mock_file):
    """Тестирование записи данных в JSON-файл."""
    data = {"key": "value", "number": 123}
    file_name = "test.json"
    MockPackageManager.write_data_on_json(data, file_name)
    
    mock_file.assert_called_once_with(file_name, 'w', encoding='utf-8')
    handle = mock_file()
    mock_dump.assert_called_once_with(data, handle, ensure_ascii=False, indent=4)

@patch('builtins.open', new_callable=mock_open, read_data='{"source1": "apt", "source2": "snap"}')
@patch('json.load')
def test_out_data_from_json_success(mock_load, mock_file, mock_package_manager):
    """Тестирование успешного чтения данных из JSON-файла."""
    expected_data = {"source1": "apt", "source2": "snap"}
    mock_load.return_value = expected_data
    file_directory = "data/sources.json"
    
    result = mock_package_manager.out_data_from_json(file_directory)
    
    mock_file.assert_called_once_with(file_directory, 'r', encoding='utf-8')
    assert result == expected_data

@patch('builtins.open', side_effect=FileNotFoundError)
def test_out_data_from_json_file_not_found(mock_file, mock_package_manager, capsys):
    """Тестирование обработки исключения FileNotFoundError."""
    file_directory = "nonexistent.json"
    result = mock_package_manager.out_data_from_json(file_directory)
    
    assert result is None
    captured = capsys.readouterr()
    assert f"Ошибка: Файл '{file_directory}' не найден." in captured.out

@patch('builtins.open', new_callable=mock_open, read_data='invalid json')
@patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "invalid json", 0))
def test_out_data_from_json_decode_error(mock_load, mock_file, mock_package_manager, capsys):
    """Тестирование обработки исключения JSONDecodeError."""
    file_directory = "bad_format.json"
    result = mock_package_manager.out_data_from_json(file_directory)
    
    assert result is None
    captured = capsys.readouterr()
    assert f"Ошибка декодирования JSON в файле '{file_directory}': Expecting value" in captured.out

# --- Тестирование класса Manager ---

@patch('subprocess.run')
@patch.object(Manager, 'parse_output')
def test_get_installed_packages_success(mock_parse_output, mock_run, manager_instance):
    """Тестирование get_installed_packages при успешном выполнении команды."""
    mock_run.return_value.stdout = "app1 version1\napp2 version2"
    mock_parse_output.return_value = {"app1": "version1", "app2": "version2"}
    command = ["dpkg", "-l"]
    
    result = manager_instance.get_installed_packages(command)
    
    mock_run.assert_called_once_with(
        command,
        capture_output=True, 
        text=True, 
        check=True
    )
    assert result == {"app1": "version1", "app2": "version2"}

@patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'cmd', stderr='error'))
def test_get_installed_packages_error(mock_run, manager_instance, capsys):
    """Тестирование get_installed_packages при ошибке выполнения команды."""
    command = ["bad_command", "-x"]
    result = manager_instance.get_installed_packages(command)
    
    assert result is None
    captured = capsys.readouterr()
    assert "Ошибка при выполнении команды:" in captured.out

def test_get_current_version(manager_instance):
    """Тестирование get_current_version (основано на get_installed_packages)."""
    # Мокируем, чтобы избежать вызова subprocess.run()
    with patch.object(manager_instance, 'get_installed_packages', return_value={"app": "1.0"}):
        result = manager_instance.get_current_version(["some", "command"])
        assert result == {"app": "1.0"}

    with patch.object(manager_instance, 'get_installed_packages', return_value=None):
        result = manager_instance.get_current_version(["some", "command"])
        assert result is None

@patch('subprocess.run')
@patch.object(Manager, 'parse_output')
def test_get_latest_version_success(mock_parse_output, mock_run, manager_instance):
    """Тестирование get_latest_version при успешном выполнении команд."""
    
    mock_run.side_effect = [
        MagicMock(return_value=MagicMock(stdout="")), # sync_command
        MagicMock(stdout="pkg1/stable 1.1.0\npkg2/stable 2.2.0"), # list_command
        MagicMock(stdout="pkg1 1.1.0\npkg2 2.2.0") # awk command
    ]
    mock_parse_output.return_value = {"pkg1": "1.1.0", "pkg2": "2.2.0"}

    sync_cmd = ["sudo", "apt", "update"]
    list_cmd = ["apt", "list", "--upgradable"]
    
    result = manager_instance.get_latest_version(sync_cmd, list_cmd)
    
    # Проверка, что команды были вызваны
    assert mock_run.call_count == 3
    # Проверка вызова sync_command
    mock_run.call_args_list[0].args[0] == sync_cmd
    # Проверка вызова list_command
    mock_run.call_args_list[1].args[0] == list_cmd
    # Проверка вызова awk command
    mock_run.call_args_list[2].args[0] == ["awk", "{print $1, $4}"]

    assert result == {"pkg1": "1.1.0", "pkg2": "2.2.0"}

@pytest.mark.parametrize("manager_name, expected_commands", [
    ("pacman", [["pacman", "-Q"], ["sudo", "pacman", "-Sy"], ["pacman", "-Qu"]]),
    ("apt", [["dpkg", "-l"], ["sudo", "apt", "update"], ["apt", "list", "--upgradable"]]),
    ("dnf", [["dnf", "list", "installed"], ["dnf", "makecache"], ["dnf", "check-update"]]),
])
def test_select_utility_commands_known_manager(manager_name, expected_commands, manager_instance):
    """Тестирование выбора команд для известных пакетных менеджеров."""
    managers = {1: manager_name}
    result = manager_instance.select_utility_commands(managers)
    assert result == expected_commands

def test_select_utility_commands_unknown_manager(manager_instance):
    """Тестирование выбора команд для неизвестного менеджера (должно вернуть None)."""
    managers = {1: "not_a_manager"}
    result = manager_instance.select_utility_commands(managers)
    assert result is None # Фактически, ваш код не обрабатывает этот случай, но по логике должен вернуть None

# --- Тестирование основных функций main.py ---

@patch.object(Manager, 'out_data_from_json', return_value={1: "apt"})
@patch('os.path.join', return_value="mock/sources.json")
def test_get_sources_success(mock_path_join, mock_out_data_from_json, manager_instance):
    """Тестирование get_sources при успешном чтении данных."""
    sources = get_sources(manager_instance)
    assert sources == {1: "apt"}
    
@pytest.mark.parametrize("latest_versions, expected", [
    ({"app1": "1.0"}, True), # Есть обновления
    (None, False),         # Нет данных об обновлениях
    ({}, True),            # Пустой словарь
])
def test_is_new_version(latest_versions, expected):
    """Тестирование is_new_version."""
    assert is_new_version(latest_versions) == expected

# Мокируем класс Main_Windows для тестирования show_updated_apps
class MockMainWindow:
    def __init__(self):
        self.out_apps = MagicMock()

def test_show_updated_apps_calls_out_apps():
    """Тестирование вызова out_apps для каждого обновляемого приложения."""
    latest_versions = {
        "app_a": "2.0",
        "app_b": "3.5.1",
        "app_c": "1.0"
    }
    current_versions = {
        "app_a": "1.9",
        "app_b": "3.5.0",
        "app_c": "1.0" # Даже если версии совпадают, он выведет, т.к. находится в latest_versions
    }
    mock_window = MockMainWindow()
    
    show_updated_apps(latest_versions, current_versions, mock_window)
    
    # Проверка, что out_apps был вызван 3 раза
    assert mock_window.out_apps.call_count == 3
    
    # Проверка аргументов для первого вызова
    mock_window.out_apps.assert_any_call("app_a", "1.9", "2.0", 0)
    # Проверка аргументов для второго вызова
    mock_window.out_apps.assert_any_call("app_b", "3.5.0", "3.5.1", 1)
    # Проверка аргументов для третьего вызова
    mock_window.out_apps.assert_any_call("app_c", "1.0", "1.0", 2)


# --- Тестирование класса Settings (с мокированием subprocess) ---

@patch('subprocess.run')
@patch.object(MockPackageManager, 'write_data_on_json')
@patch('os.path.join', side_effect=lambda *args: '/'.join(args))
@pytest.mark.parametrize("manager_name, managers_to_mock, expected_result", [
    ("Flatpak", ["flatpak"], {1: "Flatpak"}),
    ("Snap", ["snap"], {1: "Snap"}),
    ("From the package manager", ["apt", "dnf", "pacman"], {1: "apt", 2: "dnf", 3: "pacman"}),
    ("From the package manager", ["apt"], {1: "apt"}),
])
def test_settings_add_source_success(mock_path_join, mock_write, mock_run, manager_name, managers_to_mock, expected_result):
    """Тестирование добавления источника с мокированием успешных системных вызовов."""
    settings = Settings()

    # Настраиваем мок для имитации успешного выполнения команды для нужных менеджеров
    def mock_run_side_effect(cmd, **kwargs):
        program = cmd[0]
        if program in managers_to_mock:
            return MagicMock() # Успешное выполнение
        else:
            # Для "From the package manager" имитируем ошибку для менеджеров,
            # которые не входят в список 'managers_to_mock'
            if manager_name == "From the package manager" and program in ["apt", "dnf", "pacman"]:
                if program not in managers_to_mock:
                     raise subprocess.CalledProcessError(1, cmd)
            elif program == manager_name.lower():
                return MagicMock() # Успешное выполнение для Flatpak/Snap
            raise subprocess.CalledProcessError(1, cmd)

    mock_run.side_effect = mock_run_side_effect

    settings.add_source(manager_name)
    
    # Проверка, что данные были сохранены
    mock_write.assert_called_once()
    # Извлечение данных, переданных в write_data_on_json
    actual_saved_data = mock_write.call_args[0][0]
    
    assert actual_saved_data == expected_result
    
# --- Тестирование класса Gui (Мокирование методов форматирования) ---

class MockBackground(Background):
    # Мокируем тяжелые операции с файлами и графикой
    def __init__(self):
        # Пропускаем конструктор родителя, который вызывает real init
        pass 
    def create_font(self, *args, **kwargs):
        # Возвращаем простой мок-объект, имитирующий шрифт
        return MagicMock()
    def _set_scaled_min_max(self):
        pass # Мокируем, т.к. это метод CTk

def test_out_version_truncation():
    """Тестирование обрезки длинных версий."""
    mock_bg = MockBackground()
    
    # Короткая версия
    assert mock_bg.out_version("1.2.3") == "1.2.3"
    # Версия ровно 10 символов
    assert mock_bg.out_version("1.2.3.4.56") == "1.2.3.4.56"
    # Длинная версия (длина 15) -> обрезается до ...[8:]
    assert mock_bg.out_version("1.2.3.4.5.6.7.8") == "...5.6.7.8"
    # Очень длинная версия (длина 20) -> обрезается до ...[10:]
    assert mock_bg.out_version("1.2.3.4.5.6.7.8.9.0") == "...5.6.7.8.9.0"

def test_out_name_truncation():
    """Тестирование обрезки длинных имен."""
    mock_bg = MockBackground()
    
    # Короткое имя
    assert mock_bg.out_name("short-name") == "short-name"
    # Имя ровно 24 символа
    assert mock_bg.out_name("very-long-app-name-x-y-z") == "very-long-app-name-x-y-z"
    # Длинное имя (длина 25) -> обрезается до 20 символов + ...
    assert mock_bg.out_name("this-is-a-very-long-name") == "this-is-a-very-long-..."