"""Модульные тесты для проверки парсера, REPL и логики VFS эмулятора."""

import os
import tkinter as tk
from src.main import ShellEmulator

def test_env_var_expansion() -> None:
    """Проверяет корректность раскрытия системных переменных окружения."""
    root = tk.Tk()
    root.withdraw()

    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")
    os.environ["TEST_ENV_VAR"] = "HelloUNIX"

    assert emulator.expand_env_vars("echo $TEST_ENV_VAR") == "echo HelloUNIX"
    assert emulator.expand_env_vars("cd ${TEST_ENV_VAR}") == "cd HelloUNIX"

    root.destroy()

def test_missing_env_var() -> None:
    """Проверяет поведение при отсутствии переменной в системе."""
    root = tk.Tk()
    root.withdraw()

    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")
    assert emulator.expand_env_vars("echo $NOT_EXIST_VAR") == "echo $NOT_EXIST_VAR"

    root.destroy()

def test_config_paths_assignment() -> None:
    """Проверяет корректность сохранения путей конфигурации в классе."""
    root = tk.Tk()
    root.withdraw()

    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")
    assert emulator.vfs_path == "vfs.csv"
    assert emulator.script_path == "start_script.sh"

    root.destroy()

def test_vfs_navigation_cd() -> None:
    """Проверяет логику смены директорий в виртуальной файловой системе."""
    root = tk.Tk()
    root.withdraw()

    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")

    # Принудительно задаем контролируемую тестовую VFS структуру в памяти
    emulator.vfs = {
        "/": "dir",
        "/home": "dir",
        "/home/user": "dir",
        "/home/user/docs": "dir",
        "/home/user/file.txt": "file"
    }
    emulator.current_dir = "/home/user"

    # Тестируем переход в существующую дочернюю папку
    emulator.cmd_cd(["docs"])
    assert emulator.current_dir == "/home/user/docs"

    # Тестируем возврат обратно через ..
    emulator.cmd_cd([".."])
    assert emulator.current_dir == "/home/user"

    # Тестируем переход в корень
    emulator.cmd_cd(["/"])
    assert emulator.current_dir == "/"

    # Тестируем попытку зайти в файл (должно проигнорироваться)
    emulator.current_dir = "/home/user"
    emulator.cmd_cd(["file.txt"])
    assert emulator.current_dir == "/home/user"  # Путь не должен измениться

    root.destroy()