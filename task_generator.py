import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Файл для сохранения истории
HISTORY_FILE = "task_history.json"

# Предопределённые задачи с типами
TASKS = {
    "учёба": [
        "Прочитать статью по Python",
        "Решить 5 задач по алгоритмам",
        "Изучить новую тему по математике",
        "Послушать образовательный подкаст"
    ],
    "спорт": [
        "Сделать зарядку",
        "Пробежать 3 км",
        "Выполнить 50 отжиманий",
        "Позаниматься йогой 30 минут"
    ],
    "работа": [
        "Проверить электронную почту",
        "Составить план на неделю",
        "Провести совещание с командой",
        "Написать отчёт за месяц"
    ]
}

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x600")

        # Загрузка истории
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Выбор типа задачи
        type_frame = tk.Frame(self.root)
        type_frame.pack(pady=10)

        tk.Label(type_frame, text="Тип задачи:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="все")
        types = ["все"] + list(TASKS.keys())
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, values=types, state="readonly")
        type_combo.pack(side=tk.LEFT, padx=5)

        # Кнопка генерации
        generate_btn = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task)
        generate_btn.pack(pady=10)

        # Поле для отображения задачи
        self.task_label = tk.Label(self.root, text="", wraplength=450, font=("Arial", 12))
        self.task_label.pack(pady=10)

        # Добавление новой задачи
        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Новая задача:").pack(side=tk.LEFT)
        self.new_task_entry = tk.Entry(add_frame, width=30)
        self.new_task_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(add_frame, text="Тип:").pack(side=tk.LEFT)
        self.new_type_var = tk.StringVar(value="учёба")
        new_type_combo = ttk.Combobox(add_frame, textvariable=self.new_type_var,
                                     values=list(TASKS.keys()), state="readonly")
        new_type_combo.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(add_frame, text="Добавить задачу", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)

        # История задач
        history_label = tk.Label(self.root, text="История задач:")
        history_label.pack()

        self.history_listbox = tk.Listbox(self.root, width=60, height=15)
        self.history_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # Обновление списка истории
        self.update_history_display()

    def generate_task(self):
        selected_type = self.type_var.get()

        if selected_type == "все":
            all_tasks = []
            for task_list in TASKS.values():
                all_tasks.extend(task_list)
            task = random.choice(all_tasks)
        else:
            task = random.choice(TASKS[selected_type])

        # Добавляем в историю
        self.history.append(task)
        self.save_history()
        self.update_history_display()

        # Отображаем задачу
        self.task_label.config(text=task)

    def add_task(self):
        new_task = self.new_task_entry.get().strip()
        new_type = self.new_type_var.get()

        if not new_task:
            messagebox.showerror("Ошибка", "Задача не может быть пустой!")
            return

        # Добавляем задачу в соответствующий тип
        if new_type in TASKS:
            TASKS[new_type].append(new_task)
        else:
            TASKS[new_type] = [new_task]

        # Очищаем поле ввода
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Задача добавлена!")

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for i, task in enumerate(reversed(self.history[-50:]), 1):  # Последние 50 задач
            self.history_listbox.insert(0, f"{i}. {task}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
