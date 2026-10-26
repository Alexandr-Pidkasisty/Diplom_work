import tkinter as tk
import time
from datetime import datetime
import threading


def on_timer(period):
    # Создает таймер и помещает его в поток. С периодичностью, заданной в параметрах (period),
    # функция посылает событие event_time
    def worker():
        # ФУнкция для работы в потоке
        nonlocal period
        # Получаем текущее время и преобразовываем его в int
        dt = datetime.now()
        timestamp = int(dt.timestamp())  # Целое число секунд
        # Отправляем событие в главный поток
        root.event_generate("<<event_time>>", when='tail', state=timestamp)
        # Задержка перед следующим обновлением
        time.sleep(period)
        # Создаем замыкание
        worker()
    # Запускаем поток
    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


# Привязываем обработчик события
def on_event(event):
    dt = datetime.fromtimestamp(event.state)
    lbl.config(text=f"Вызываем нужную функцию и выводим штамп времени: {dt}")

def on_button():
    time_period = entry.get().strip()
    corrected_text = ''.join((b for b in time_period if b in '0123456789'))
    tm = int(corrected_text)
    on_timer(tm)


# В основном потоке
root = tk.Tk()
entry = tk.Entry(root)
entry.pack()


btn = tk.Button(root, text="Включить таймер", command=on_button)
btn.pack()

lbl = tk.Label(root, text="Старт")
lbl.pack()

root.bind("<<event_time>>", on_event)

root.mainloop()
