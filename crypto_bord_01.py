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
    global coins_ident
    global var_chb
    modal_window = Toplevel(root)
    modal_window.title("Выбор криптовалют для отслеживания")

    frame_modal_w = Frame(modal_window, bg='light grey')
    frame_modal_w.pack(fill="x", padx=10, pady=5)
    
    # Здесь можно добавить виджеты (кнопки, поля ввода и т.д.)

    # Label(frame_modal_w, text='   bitcoin', image=coins_ident.get("bitcoin"), compound=LEFT, width=200, justify="left", anchor="w").pack(padx=10, anchor="w")
    # Label(frame_modal_w, text='   ethereum', image=coins_ident.get("ethereum"), compound=LEFT, width=200, justify="left", anchor="w").pack(padx=10, anchor="w")

    # Создаем метки с изображением и названием криптовалюты и чекбоксы для их выбора
    for i, key in enumerate(coins_ident):
        Label(frame_modal_w, text=f"  {key}", image=coins_ident.get(key), compound=LEFT,
              width=200, justify="left", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky ="w") 
        # tmp_var = IntVar()
        Checkbutton(frame_modal_w, variable=var_chb[i]).grid(row=i, column=1, padx=5, pady=5, sticky ="w")
    

    Button(frame_modal_w, text="Закрыть", command=modal_window.destroy).grid(row=len(coins_ident), column=1, padx=5, pady=5, sticky ="w")
  
    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна

root_scr_size = [620, 520]          # начальный размер корневого окна
menu_flag = True                    # флаг видимости рамки, строки заголовка и меню окна

# Главное окно программы
root = Tk()
root.title("Курсы криптовалют")
root.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")

frame_root = Frame(root, bg='gray')
frame_root.pack(fill="x", padx=10, pady=5)

# Перечень криптовалют с аватарками
coins_ident = {
    "bitcoin" : ImageTk.PhotoImage(Image.open("images/bitcoin.webp").resize((30, 30))),
    "ethereum" : ImageTk.PhotoImage(Image.open("images/ethereum.webp").resize((30, 30)))
}

# Перечень криптовалют с курсами
coins_rate = {
    "bitcoin" : "82,852.91",
    "ethereum" : "2,496.02"
}

 # Список индикаторных переменных для выбора отслеживаемых валют
var_chb = [IntVar() for _ in range(len(coins_ident))]

# Метки с выбранными криптовалютами


root.bind("<Double-Button-1>", lambda event: hide_menu(event) if menu_flag else show_menu(event))
# Двойной клик по окну скрывает рамку, строку заголовка и меню окна

# Основное меню
menu_bar = Menu(root)
root.config(menu=menu_bar)

settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Настройки', menu=settings_menu)
settings_menu.add_command(label="Справочник", command=open_modal)
# settings_menu.add_command(label="Сохранить", command=settings_save)
# settings_menu.add_command(label="Удалить", command=settings_delete)
# settings_menu.add_separator()
settings_menu.add_command(label="Выход", command=quit)

# Отладка
# Кнопка для вывода значений
# def print_values():
#     values = [var.get() for var in var_chb]
#     print(values)
    
# btn = Button(frame_root, text='Печать', command=print_values)
# btn.grid(row=len(coins_ident)+1, column=1)
# Отладка

root.mainloop()