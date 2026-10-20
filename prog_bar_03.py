import tkinter as tk
from tkinter import ttk
import time

def update_progress(progress_bar, total, callback):
    """Обновляет Progressbar и вызываемую функцию при каждом шаге"""
    def step():
        nonlocal progress_bar
        current = progress_bar['value']
        # Вычисляем процент и обновляем индикатор
        progress_bar['value'] = current + 1
        percentage = round((current + 1) / total * 100)
        # Обновляем текст над прогрессбаром (например, в метке)
        style.configure('text.Horizontal.TProgressbar', text=f'{percentage}%')
        root.update_idletasks()  # Обязательно: обновляем интерфейс сразу
        callback()  # Вызываем callback, если нужно

    step()  # Запуск первой итерации

# Создаём окно
root = tk.Tk()
root.title("Прогрессбар пример")

# Создаём стиль для отображения текста
style = ttk.Style(root)
style.configure('text.Horizontal.TProgressbar', text='0%')  # Начальное значение

# Создаём прогрессбар
progress_bar = ttk.Progressbar(root, length=200, mode='determinate', maximum=100, value=0)
progress_bar.pack()

# Пример callback-функции
def on_step():
    print("Выполняется задача...")

# Запускаем процесс с обновлением прогресса
update_progress(progress_bar, 100, on_step)

root.mainloop()
