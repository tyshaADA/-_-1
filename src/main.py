"""Модуль GUI-эмулятора командной строки UNIX-подобной ОС.

Реализует интерактивное окно терминала (REPL) для Варианта №2.
"""

import os
import re
import socket
import sys
import tkinter as tk


class ShellEmulator:
    """Класс графического интерфейса и логики эмулятора оболочки."""

    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует главное окно и компоненты GUI."""
        self.root = root
        self.setup_window()
        self.create_widgets()

    def setup_window(self) -> None:
        """Настраивает параметры графического окна и его заголовок."""
        username = os.getlogin()
        hostname = socket.gethostname()
        # Заголовок строго по требованию: Эмулятор - [username@hostname]
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
        self.output_text.insert(tk.END, "Добро пожаловать в эмулятор оболочки!\n")
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

    def expand_env_vars(self, line: str) -> str:
        """Раскрывает переменные окружения вида $VAR или ${VAR}."""
        def replacer(match: re.Match) -> str:
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, match.group(0))

        pattern = r"\$(?:{([A-Za-z0-9_]+)}|([A-Za-z0-9_]+))"
        return re.sub(pattern, replacer, line)

    def handle_command(self, event: tk.Event) -> None:
        """Парсит и обрабатывает введенную пользователем команду."""
        raw_input = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not raw_input:
            return

        self.append_output(f"$ {raw_input}")
        expanded_input = self.expand_env_vars(raw_input)
        tokens = expanded_input.split()

        cmd = tokens[0]
        args = tokens[1:]

        if cmd == "exit":
            self.root.quit()
            sys.exit(0)
        elif cmd in ("ls", "cd"):
            self.append_output(f"[Заглушка] Команда: {cmd}, Аргументы: {args}")
        else:
            self.append_output(f"Ошибка: неизвестная команда '{cmd}'")


def main() -> None:
    """Точка входа в приложение эмулятора."""
    root = tk.Tk()
    ShellEmulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

