import tkinter as tk
from tkinter import messagebox

# Создаём модальное окно (Toplevel)
modal_window = tk.Toplevel()
modal_window.title("Модальное окно")

# Функция, которая будет вызвана при нажатии на крестик
def on_closing():
    # Можно добавить проверку, например, запрос на сохранение данных
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите закрыть окно?"):
        modal_window.destroy()  # Закрываем окно, если пользователь подтвердил

# Привязываем функцию к событию закрытия
modal_window.protocol("WM_DELETE_WINDOW", on_closing)

# Опциональная кнопка для явного закрытия (для удобства)
btn_close = tk.Button(modal_window, text="Закрыть", command=modal_window.destroy)
btn_close.pack()

modal_window.mainloop()
