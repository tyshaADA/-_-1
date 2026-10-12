"""Модульные тесты для проверки парсера, REPL и логики всех команд эмулятора."""

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
    root.destroy()

def test_vfs_navigation_cd() -> None:
    """Проверяет логику смены директорий в виртуальной файловой системе."""
    root = tk.Tk()
    root.withdraw()
    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")
    emulator.vfs = {
        "/": {"type": "dir", "size": 0, "mode": "755"},
        "/home": {"type": "dir", "size": 0, "mode": "755"},
        "/home/user": {"type": "dir", "size": 0, "mode": "755"},
        "/home/user/docs": {"type": "dir", "size": 0, "mode": "755"},
    }
    emulator.current_dir = "/home/user"
    emulator.cmd_cd(["docs"])
    assert emulator.current_dir == "/home/user/docs"
    root.destroy()

def test_command_rev() -> None:
    """Проверяет корректность работы утилиты разворота строк rev."""
    root = tk.Tk()
    root.withdraw()
    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")

    # Перехватываем вывод
    output_lines = []
    emulator.append_output = lambda text: output_lines.append(text)

    emulator.cmd_rev(["hello", "world"])
    assert "dlrow olleh" in output_lines
    root.destroy()

def test_command_chmod() -> None:
    """Проверяет корректность изменения прав доступа с помощью chmod."""
    root = tk.Tk()
    root.withdraw()
    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")
    emulator.vfs = {"/home/user/notes.txt": {"type": "file", "size": 100, "mode": "644"}}
    emulator.current_dir = "/home/user"

    emulator.cmd_chmod(["755", "notes.txt"])
    assert emulator.vfs["/home/user/notes.txt"]["mode"] == "755"
    root.destroy()

def test_command_du() -> None:
    """Проверяет вычисление занимаемого места du."""
    root = tk.Tk()
    root.withdraw()
    emulator = ShellEmulator(root, "vfs.csv", "start_script.sh")
    emulator.vfs = {"/home/user/notes.txt": {"type": "file", "size": 500, "mode": "644"}}
    emulator.current_dir = "/home/user"

    output_lines = []
    emulator.append_output = lambda text: output_lines.append(text)

    emulator.cmd_du(["notes.txt"])
    assert "500\tnotes.txt" in output_lines
    root.destroy()