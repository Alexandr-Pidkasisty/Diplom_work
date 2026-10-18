import tkinter as tk

root = tk.Tk()  # Создаём главное окно

# Создаём переменную, которая будет хранить состояние (1 — включено, 0 — выключено)
var = tk.BooleanVar()

# Создаём сам флажок
checkbutton = tk.Checkbutton(root, text="Согласен на рассылку", variable=var, onvalue=True, offvalue=False)
checkbutton.pack(pady=10)  # Размещаем виджет в окне с отступами
print(var.get())
root.mainloop()  # Запускаем цикл событий