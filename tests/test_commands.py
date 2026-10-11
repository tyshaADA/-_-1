"""Модульные тесты для проверки парсера и REPL эмулятора оболочки."""

import os
import tkinter as tk
from src.main import ShellEmulator

def test_env_var_expansion() -> None:
    """Проверяет корректность раскрытия системных переменных окружения."""
    root = tk.Tk()
    root.withdraw()  # Скрываем реальное окно графического интерфейса

    emulator = ShellEmulator(root)
    os.environ["TEST_ENV_VAR"] = "HelloUNIX"

    # Тест обычного формата $VAR
    assert emulator.expand_env_vars("echo $TEST_ENV_VAR") == "echo HelloUNIX"
    # Тест сложного формата ${VAR}
    assert emulator.expand_env_vars("cd ${TEST_ENV_VAR}") == "cd HelloUNIX"

    root.destroy()  # Освобождаем графические ресурсы окна после теста

def test_missing_env_var() -> None:
    """Проверяет поведение при отсутствии переменной в системе."""
    root = tk.Tk()
    root.withdraw()  # Скрываем окно терминала

    emulator = ShellEmulator(root)
    # Если переменной нет, строка должна остаться неизменной
    assert emulator.expand_env_vars("echo $NOT_EXIST_VAR") == "echo $NOT_EXIST_VAR"

    root.destroy()  # Закрываем ресурсы
