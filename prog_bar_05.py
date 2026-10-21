import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
from functools import partial

def worker(q, root):
    for i in range(100):
        # Передаём текущее значение в очередь
        q.put(i + 1)
        # Генерируем событие для обновления виджета
        root.event_generate('<<Updated>>', when='tail')
        time.sleep(0.1)

def on_update(event, q, pb):
    # Получаем значение из очереди и обновляем прогресс-бар
    pb['value'] = q.get()

# Создаём очередь для обмена данными
q = queue.Queue()

# Создаём окно и прогресс-бар
root = tk.Tk()
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')
progress_bar.pack()

# Связываем обработчик события
root.bind('<<Updated>>', partial(on_update, q=q, pb=progress_bar))

# Запускаем поток
t = threading.Thread(target=worker, args=(q, root))
t.start()

root.mainloop()
