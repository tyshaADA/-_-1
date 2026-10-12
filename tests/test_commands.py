"""Модульные тесты для проверки парсера и REPL эмулятора оболочки."""

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

    test_vfs = "custom_vfs.csv"
    test_script = "custom_script.sh"
    emulator = ShellEmulator(root, test_vfs, test_script)

    # Проверяем, что пути правильно записались в переменные объекта
    assert emulator.vfs_path == test_vfs
    assert emulator.script_path == test_script

    root.destroy()
