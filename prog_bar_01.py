import tkinter as tk
from tkinter import ttk
import time

def start_loading():
    progress_bar['value'] = 0  # Сброс индикатора
    window.update_idletasks()  # Принудительное обновление интерфейса
    for i in range(101):
        progress_bar['value'] = i  # Обновление значения
        window.update_idletasks()  # Обновление интерфейса
        time.sleep(0.05)  # Имитация задержки (например, обработка данных)
    label.config(text="Загрузка завершена")  # Обновление метки после завершения

# Создание основного окна
window = tk.Tk()
window.title("Индикатор загрузки")

# Создание метки
label = tk.Label(window, text="Загрузка...")
label.pack(pady=10)

# Создание индикатора загрузки
progress_bar = ttk.Progressbar(
    window,
    orient='horizontal',
    length=300,
    mode='determinate'  # Определённый режим (точный прогресс)
)
progress_bar.pack(pady=20)

# Кнопка для запуска загрузки
start_button = tk.Button(window, text="Начать загрузку", command=start_loading)
start_button.pack(pady=10)

# Запуск главного цикла
window.mainloop()
