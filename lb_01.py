import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Scrollable Listbox")

# Создаём контейнер (фрейм) для Listbox и Scrollbar
frame = ttk.Frame(root)
frame.pack(expand=True, fill="both")

# Создаём вертикальную Scrollbar
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Создаём Listbox и связываем его с Scrollbar
listbox = tk.Listbox(frame, selectmode="multiple", yscrollcommand=scrollbar.set)
listbox.pack(side=tk.LEFT, fill="both", expand=True)

# Настраиваем Scrollbar, чтобы он управлял прокруткой Listbox
scrollbar.config(command=listbox.yview)

# Заполняем Listbox элементами
for i in range(100):
    listbox.insert(tk.END, f"Элемент {i}")



root.mainloop()
