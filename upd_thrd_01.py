import tkinter as tk
import threading
import time


def update_widget():
    #Здесь логика вычисления нового значения
    new_text = int(time.time())
    # Отправляем событие в главный поток
    root.event_generate("<<event1>>", when='tail', state=new_text)
    # Задержка перед следующим обновлением
    time.sleep(1)
    # Создаем замыкание
    update_widget()

# В основном потоке
root = tk.Tk()
lbl = tk.Label(root, text="Старт")
lbl.pack()

# Привязываем обработчик события
def on_event(event):
    lbl.config(text=event.state)

root.bind("<<event1>>", on_event)

# Запускаем поток
thread = threading.Thread(target=update_widget, daemon=True)
thread.start()

root.mainloop()
