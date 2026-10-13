from tkinter import *
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageGrab
import json
import os
import requests


def quit():
    root.destroy()

def coins_rate_request():
    return requests.get("https://api.coinlore.net/api/tickers/",
                        params={"start":0, "limit":100})


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

    def on_selection_change(event):
        global selected_indices
        tmp = lst_coins.curselection()
        selected_indices = [lst_coins.get(i) for i in tmp]
        # print("Выбранные валюты: ", selected_indices)

    # Создаём дочернее модальное окно с настройками. Сохраняем настройки в глобальных переменных и закрываем
    # модальное окно. Затем создаем виджеты на главном окне.
    global coins_ident
    global var_chb
    modal_window = Toplevel(root)
    modal_window.title("Справочник криптовалют")

    frame_modal_w = Frame(modal_window)
    frame_modal_w.pack(fill="x", padx=10, pady=5)

    # Создаем заголовок
    # Label(frame_modal_w, text='Название криптовалюты', compound=LEFT, 
    #       justify="left", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky ="w")
    # Label(frame_modal_w, text='В избранное', compound=LEFT, 
    #           justify="left", anchor="w").grid(row=0, column=1, padx=5, pady=5, sticky ="w")
    
    # Создаем метки с изображением и названием криптовалюты и чекбоксы для их выбора
    # for i, key in enumerate(coins_ident):
    #     Label(frame_modal_w, text=f"  {key}", image=coins_ident.get(key), compound=LEFT,
    #           width=200, justify="left", anchor="w").grid(row=i+1, column=0, padx=5, pady=5, sticky ="w") 
    #     Checkbutton(frame_modal_w, variable=var_chb[i], onvalue=True, offvalue=False).grid(row=i+1, column=1, padx=5, pady=5, sticky ="w")
    
    # Создаём Listbox
    lst_coins = Listbox(frame_modal_w, width=50, selectmode=MULTIPLE)
    lst_coins.pack(side='left', fill='both', expand=True)

    # Создаём Scrollbar
    scroll = Scrollbar(frame_modal_w, orient=VERTICAL)  # Полоса прокрутки вертикальная
    scroll.pack(side=RIGHT, fill=Y)                     # Заполнение по высоте

    # Связываем Scrollbar и Listbox
    scroll.config(command=lst_coins.yview)      # Scrollbar управляет прокруткой Listbox
    lst_coins.config(yscrollcommand=scroll.set) # Listbox сообщает Scrollbar о текущем положении

    # Получаем данные о криптовалютах и вводим их наименования в список выбора
    coins_ident = coins_rate_request()
    for coin in coins_ident.json()["data"]:
        lst_coins.insert(END, f'{coin["name"]} ({coin["symbol"] })')

      # Получаем список выбранных валют

    lst_coins.bind("<<ListboxSelect>>", on_selection_change)
    


    # Button(frame_modal_w, text="Закрыть", command=modal_window.destroy).grid(row=len(coins_ident)+1, column=1, padx=5, pady=5, sticky ="w")
    
    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна

    print("Индексы выбранных валют: ", selected_indices)
    # create_labels()                 # Вызываем функцию для создания виджетов в главном окне

    # tmp = [value.get() for value in var_chb]    # Создаем временный список типа bool из списка var_chb
    # save_json_safely(tmp, var_chb_filename)     # Сохраняем список tmp


def clear_frame_root():
    # Очищаем главное окно от виджетов
    if frame_root.winfo_children():                 # Проверяем наличие виджетов в главном окне
        for widget in frame_root.winfo_children():  # Если виджеты есть,
            widget.destroy()                        # то удаляем их
        

def create_labels():
    # Создание виджетов в главном окне: выводятся избранные криптовалюты и их курсы
    global selected_indices
    clear_frame_root()  # Очищаем главное окно от виджетов
    # for value in selected_indices.json()["data"]:
    #     Label(frame_root, text=f"  {value["name"]} ({value["symbol"]})", compound=LEFT,
    #               width=200, justify="left", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky ="w")
    #     Label(frame_root, text=f"  ${value["price_usd"]}", compound=LEFT,
    #                   width=20, justify="left", anchor="w").grid(row=i, column=1, padx=5, pady=5, sticky ="w")


def save_json_safely(data, filename):
    # Функция сериализует данные из data в файл с именем filename
    try:
        # Создаём директорию, если её нет
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        # Сохраняем файл
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except TypeError as e:
        return False, mb.showerror("Ошибка", f"Ошибка типа данных: {str(e)}")
    except (PermissionError, OSError) as e:
        return False, mb.showerror("Ошибка", f"Ошибка записи файла: {str(e)}")


def load_json_safely(filename):
    # Функция возвращает данные из файла с именем filename
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None, mb.showinfo("Информация", f"Файл {filename} не найден.\nБудет создан новый файл")  # Возвращает список (None "ok")
    except json.JSONDecodeError:
        return None, mb.showerror("Ошибка", "Ошибка декодирования JSON")   # Возвращает список (None "ok")
    

# ********************************************************************************************************************

# root_scr_size = [620, 520]            # начальный размер корневого окна
menu_flag = True                        # флаг видимости рамки, строки заголовка и меню окна
var_chb_filename = "data/var_chb.json"  # Имя файла для сохранения/ востсановления флагов избранного
image = 'My_web_01.ico'

# Главное окно программы
root = Tk()
root.title("Курсы криптовалют")
# root.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")
root.minsize(300, 50)  # Задал минимальный размер окна
root.iconbitmap(image)

frame_root = Frame(root, bg='gray')
frame_root.pack(fill="x", padx=10, pady=5)

# Перечень криптовалют с аватарками
coins_ident = []
selected_indices = []
# try:
#     coins_ident = {
#         "Bitcoin BTC" : ImageTk.PhotoImage(Image.open("images/bitcoin.webp").resize((30, 30))),
#         "Ethereum ETH" : ImageTk.PhotoImage(Image.open("images/ethereum.webp").resize((30, 30))),
#         "Tether USDT" : ImageTk.PhotoImage(Image.open("images/tether.webp").resize((30, 30)))
#     }
# except FileNotFoundError:
#     mb.showerror('Ошибка', 'Файлы с аватарами криптовалют не найдены')
# except Exception as ex:
#     mb.showerror('Ошибка', f'При открытии файлов произошла ошибка {ex}')

# Перечень криптовалют с курсами
coins_rate = {
    "Bitcoin BTC" : "82,852.91",
    "Ethereum ETH" : "2,496.02",
    "Tether USDT" : "0.9992"
}

# Восстанавливаем из файла/ создаем список индикаторных переменных для выбора отслеживаемых валют.
#  Создаем виджеты с избранными криптовалютами
var_chb = [BooleanVar() for _ in range(len(coins_ident))]   # Создаем пустой список
tmp = load_json_safely(var_chb_filename)                    # Пытаемся загрузить значения из файла во временный список
print(tmp)
if tmp[0] is not None:                                      # Если временный список из файла прочитан, то
    for i in range(len(var_chb)):                           # Меняем значения списка var_chb на значения из
        var_chb[i].set(tmp[i])                              # временного списка
    create_labels()                                         # Вызываем функцию для создания виджетов в главном окне

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