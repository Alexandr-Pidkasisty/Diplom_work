import tkinter as tk
import threading
import time

def worker_thread(root, data):
    # Имитация длительной задачи
    time.sleep(5)
    # Отправляем событие в основной поток
    root.event_generate("<<DataUpdated>>", when='tail', state=data)

def update_label(event):
    # Этот обработчик выполняется в основном потоке
    label.config(text=f"Данные: {event.state}")

# Создание главного окна
root = tk.Tk()
label = tk.Label(root, text='Старт')
label.pack()

# Привязка обработчика к событию
root.bind("<<DataUpdated>>", update_label)

# Запуск фонового потока
thread = threading.Thread(target=worker_thread, args=(root, 42))
thread.start()

root.mainloop()
