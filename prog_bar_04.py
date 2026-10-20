import tkinter as tk
from tkinter import ttk

def create_ui(root):
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = ttk.Label(frame, text="Исходный текст")
    label.pack()

    btn = ttk.Button(frame, text="Обновить", command=lambda: update_label(label))
    btn.pack(pady=5)

    return label  # можно вернуть, если понадобится где-то ещё

def update_label(lbl):
    lbl.config(text="Текст обновлён!")

root = tk.Tk()
root.title("Пример обновления Label")
create_ui(root)
root.mainloop()