from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageGrab


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
    # Создаём дочернее модальное окно с настройками. Сохраняем настройки в глобальных переменных и закрываем
    # модальное окно. Затем создаем виджеты на главном окне.
    global coins_ident
    global var_chb
    modal_window = Toplevel(root)
    modal_window.title("Выбор криптовалют для отслеживания")

    frame_modal_w = Frame(modal_window, bg='light grey')
    frame_modal_w.pack(fill="x", padx=10, pady=5)
    
    # Создаем метки с изображением и названием криптовалюты и чекбоксы для их выбора
    for i, key in enumerate(coins_ident):
        Label(frame_modal_w, text=f"  {key}", image=coins_ident.get(key), compound=LEFT,
              width=200, justify="left", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky ="w") 
        Checkbutton(frame_modal_w, variable=var_chb[i], onvalue=True, offvalue=False).grid(row=i, column=1, padx=5, pady=5, sticky ="w")
    
    # Button(frame_modal_w, text="Закрыть", command=modal_window.destroy).grid(row=len(coins_ident), column=1, padx=5, pady=5, sticky ="w")
    
    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна
    
    create_labels()                 # Вызываем функцию для создания виджетов в главном окне


def clear_frame_root():
    # Очищаем главное окно от виджетов
    if frame_root.winfo_children():                 # Проверяем наличие виджетов в главном окне
        for widget in frame_root.winfo_children():  # Если виджеты есть,
            widget.destroy()                        # то удаляем их
        

def create_labels():
    # Создание виджетов в главном окне: выводятся избранные криптовалюты и их курсы
    global var_chb
    clear_frame_root()  # Очищаем главное окно от виджетов
    for i, key in enumerate(coins_ident):
        if var_chb[i].get():
            Label(frame_root, text=f"  {key}", image=coins_ident.get(key), compound=LEFT,
                  width=200, justify="left", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky ="w")
            Label(frame_root, text=f"  {coins_rate.get(key)}", compound=LEFT,
                      width=40, justify="left", anchor="w").grid(row=i, column=1, padx=5, pady=5, sticky ="w")


# ********************************************************************************************************************

# root_scr_size = [620, 520]          # начальный размер корневого окна
menu_flag = True                    # флаг видимости рамки, строки заголовка и меню окна

# Главное окно программы
root = Tk()
root.title("Курсы криптовалют")
# root.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")
root.minsize(300, 150)

frame_root = Frame(root, bg='gray')
frame_root.pack(fill="x", padx=10, pady=5)

# Перечень криптовалют с аватарками
try:
    coins_ident = {
        "Bitcoin BTC" : ImageTk.PhotoImage(Image.open("images/bitcoin.webp").resize((30, 30))),
        "Ethereum ETH" : ImageTk.PhotoImage(Image.open("images/ethereum.webp").resize((30, 30))),
        "Tether USDT" : ImageTk.PhotoImage(Image.open("images/tether.webp").resize((30, 30)))
    }
except FileNotFoundError:
    mb.showerror('Ошибка', 'Файлы с аватарами криптовалют не найдены')
except Exception as ex:
    mb.showerror('Ошибка', f'При открытии файлов произошла ошибка {ex}')

# Перечень криптовалют с курсами
coins_rate = {
    "Bitcoin BTC" : "82,852.91",
    "Ethereum ETH" : "2,496.02",
    "Tether USDT" : "0.9992"
}

# Список индикаторных переменных для выбора отслеживаемых валют
var_chb = [BooleanVar() for _ in range(len(coins_ident))]

# Двойной клик по окну скрывает рамку, строку заголовка и меню окна
root.bind("<Double-Button-1>", lambda event: hide_menu(event) if menu_flag else show_menu(event))

# Основное меню
menu_bar = Menu(root)
root.config(menu=menu_bar)

settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Настройки', menu=settings_menu)
settings_menu.add_command(label="Справочник", command=open_modal)
settings_menu.add_separator()
settings_menu.add_command(label="Выход", command=quit)

# Отладка
# Кнопка для вывода значений
# def print_values():
#     values = [var.get() for var in var_chb]
#     print(values)
    
# btn = Button(root, text='Печать', command=print_values)
# btn.pack()
# btn1 = Button(root, text='Обновить', command=create_labels)
# btn1.pack()
# Отладка

root.mainloop()