"""Модуль GUI-эмулятора командной строки UNIX-подобной ОС.

Реализует интерактивное окно терминала и чтение конфигурации для Варианта №2.
"""

import argparse
import os
import re
import socket
import sys
import tkinter as tk

class ShellEmulator:
    """Класс графического интерфейса и логики эмулятора оболочки."""

    def __init__(self, root: tk.Tk, vfs_path: str, script_path: str) -> None:
        """Инициализирует окно, параметры конфигурации и компоненты GUI."""
        self.root = root
        self.vfs_path = vfs_path
        self.script_path = script_path

        self.setup_window()
        self.create_widgets()
        self.print_debug_info()
        self.execute_start_script()

    def setup_window(self) -> None:
        """Настраивает параметры графического окна и его заголовок."""
        username = os.getlogin()
        hostname = socket.gethostname()
        self.root.title(f"Эмулятор - [{username}@{hostname}]")
        self.root.geometry("700x450")
        self.root.configure(bg="#1e1e1e")

    def create_widgets(self) -> None:
        """Создает элементы текстового вывода и строку ввода."""
        self.output_text = tk.Text(
            self.root, bg="#1e1e1e", fg="#33ff33",
            insertbackground="#33ff33", font=("Courier", 11)
        )
        self.output_text.pack(expand=True, fill="both", padx=5, pady=5)
        self.output_text.insert(tk.END, "Добро пожаловать в эмулятор!\n")
        self.output_text.config(state=tk.DISABLED)

        self.input_entry = tk.Entry(
            self.root, bg="#2d2d2d", fg="#ffffff",
            insertbackground="#ffffff", font=("Courier", 11)
        )
        self.input_entry.pack(fill="x", padx=5, pady=5)
        self.input_entry.bind("<Return>", self.handle_command)
        self.input_entry.focus_set()

    def append_output(self, text: str) -> None:
        """Добавляет текст в область лога терминала."""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)

    def print_debug_info(self) -> None:
        """Выводит отладочную информацию о параметрах конфигурации при старте."""
        self.append_output("=== ОТЛАДОЧНАЯ ИНФОРМАЦИЯ КОНФИГУРАЦИИ ===")
        self.append_output(f"Путь к VFS (файловая система): {self.vfs_path}")
        self.append_output(f"Путь к стартовому скрипту: {self.script_path}")
        self.append_output("==========================================\n")

    def execute_start_script(self) -> None:
        """Последовательно считывает и выполняет команды из стартового скрипта."""
        if not self.script_path or not os.path.exists(self.script_path):
            return

        self.append_output(f"Запуск стартового скрипта: {self.script_path}")
        try:
            with open(self.script_path, "r", encoding="utf-8") as file:
                for line in file:
                    cleaned_line = line.strip()
                    # Пропускаем пустые строки и комментарии
                    if not cleaned_line or cleaned_line.startswith("#"):
                        continue
                    # Имитируем ввод пользователя и выполнение команды
                    self.append_output(f"$ {cleaned_line}")
                    self.process_command(cleaned_line)
        except Exception as err:
            self.append_output(f"Ошибка чтения скрипта: {err}")

    def expand_env_vars(self, line: str) -> str:
        """Раскрывает переменные окружения вида $VAR или ${VAR}."""
        def replacer(match: re.Match) -> str:
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, match.group(0))

        pattern = r"\$(?:{([A-Za-z0-9_]+)}|([A-Za-z0-9_]+))"
        return re.sub(pattern, replacer, line)

    def process_command(self, raw_input: str) -> None:
        """Выполняет разбор строки ввода и обрабатывает конкретную команду."""
        expanded_input = self.expand_env_vars(raw_input)
        tokens = expanded_input.split()
        if not tokens:
            return

        cmd = tokens[0]
        args = tokens[1:]

        if cmd == "exit":
            self.root.quit()
            sys.exit(0)
        elif cmd in ("ls", "cd"):
            self.append_output(f"[Заглушка] Команда: {cmd}, Аргументы: {args}")
        else:
            self.append_output(f"Ошибка: неизвестная команда '{cmd}'")

    def handle_command(self, event: tk.Event) -> None:
        """Парсит и обрабатывает введенную пользователем команду из GUI."""
        raw_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not raw_input:
            return

        self.append_output(f"$ {raw_input}")
        self.process_command(raw_input)

def main() -> None:
    """Точка входа в приложение эмулятора."""
    parser = argparse.ArgumentParser(
        description="GUI-эмулятор командной строки UNIX."
    )
    # Обязательные аргументы по заданию
    parser.add_argument(
        "--vfs", required=True, help="Путь к физическому расположению VFS"
    )
    parser.add_argument(
        "--script", required=True, help="Путь к стартовому скрипту сценария"
    )

    parsed_args = parser.parse_args()

    root = tk.Tk()
    ShellEmulator(root, parsed_args.vfs, parsed_args.script)
    root.mainloop()

if __name__ == "__main__":
    main()
