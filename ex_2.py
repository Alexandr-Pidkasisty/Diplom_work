import tkinter as tk
from tkinter import messagebox

def on_closing():
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
        root.destroy()

root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", lambda: on_closing())  # Регистрируем обработчик
root.mainloop()
