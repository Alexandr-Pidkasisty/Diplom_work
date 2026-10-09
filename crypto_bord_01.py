from tkinter import*
from PIL import Image, ImageTk, ImageGrab

def settings_open():
    pass


def settings_save():
    pass


def settings_delete():
    pass


def quit():
    root.destroy()


def hide_menu(event):
    # Скрываем рамку, строку заголовка и меню окна
    global menu_flag
    empty_menu = Menu(root)         # создаём пустое меню
    root.config(menu=empty_menu)    # заменяем действующее меню на пустое
    root.overrideredirect(True)     # удаляем рамку и строку заголовка
    menu_flag = False               # меняем флаг корневого окна


def show_menu(event):
    # Восстанавливаем рамку, строку заголовка и меню окна
    global menu_flag
    root.config(menu=menu_bar)      # возвращаем действующее меню
    root.overrideredirect(False)    # возвращаем рамку и строку заголовка
    menu_flag = True                # меняем флаг корневого окна 


def open_modal():
    # Создаём дочернее модальное окно с настройками
    global cryptos
    modal_window = Toplevel(root)
    modal_window.title("Модальное окно")
    modal_window.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")

    frame_modal_w = Frame(modal_window, bg='light grey')
    frame_modal_w.pack(fill="x", padx=10, pady=5)
    
    # Здесь можно добавить виджеты (кнопки, поля ввода и т.д.)

    # Label(frame_modal_w, text='   bitcoin', image=cryptos.get("bitcoin"), compound=LEFT, width=200, justify="left", anchor="w").pack(padx=10, anchor="w")
    # Label(frame_modal_w, text='   ethereum', image=cryptos.get("ethereum"), compound=LEFT, width=200, justify="left", anchor="w").pack(padx=10, anchor="w")

    # Создаем метки с изображением и названием криптовалюты
    for i, key in enumerate(cryptos):
        Label(frame_modal_w, text=f"  {key}", image=cryptos.get(key), compound=LEFT, width=200, justify="left", anchor="w").pack(padx=5, pady=5, anchor="w") 


    Button(frame_modal_w, text="Закрыть", command=modal_window.destroy).pack()
    
    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна

root_scr_size = [620, 520]          # начальный размер корневого окна
menu_flag = True                    # флаг видимости рамки, строки заголовка и меню окна


root = Tk()
root.title("Курсы криптовалют")
root.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")

frame_root = Frame(root, bg='gray')
frame_root.pack(fill="x", padx=10, pady=5)



cryptos = {
    "bitcoin" : ImageTk.PhotoImage(Image.open("images/bitcoin.webp").resize((30, 30))),
    'ethereum' : ImageTk.PhotoImage(Image.open("images/ethereum.webp").resize((30, 30)))
}

# Label(frame_root, text='bitcoin', image=cryptos.get("bitcoin")).pack(padx=10)
# Label(frame_root, text='ethereum', image=cryptos.get("ethereum")).pack(padx=10)

root.bind("<Double-Button-1>", lambda event: hide_menu(event) if menu_flag else show_menu(event))
# Двойной клик по окну скрывает рамку, строку заголовка и меню окна

menu_bar = Menu(root)
root.config(menu=menu_bar)

settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Настройки', menu=settings_menu)
settings_menu.add_command(label="Открыть", command=open_modal)
# settings_menu.add_command(label="Сохранить", command=settings_save)
# settings_menu.add_command(label="Удалить", command=settings_delete)
# settings_menu.add_separator()
settings_menu.add_command(label="Выход", command=quit)

root.mainloop()