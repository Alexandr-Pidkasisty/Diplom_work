from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import json
import os
import requests
from datetime import datetime
import pickle


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
  

def clear_frame_root():
    # Функция очистки главного окна от виджетов
    if frame_root.winfo_children():                 # Проверяем наличие виджетов в главном окне
        for widget in frame_root.winfo_children():  # Если виджеты есть,
            widget.destroy()                        # то удаляем их
    if frame_footer.winfo_children():                   # Проверяем наличие виджетов в футоре
        for widget in frame_footer.winfo_children():    # Если виджеты есть,
            widget.destroy()                            # то удаляем их

def create_labels():
    # Функция создания виджетов в главном окне: выводятся избранные криптовалюты и их курсы
    global favourites_coins_fname
    global time_stamp
    clear_frame_root()  # Очищаем главное окно от виджетов
    favourites = load_json_safely(favourites_coins_fname)
    try:
        with open(time_stamp_fname, 'r', encoding='utf-8') as f:
            time_stamp = f.read()
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке открыть файл {time_stamp_fname} произошла ошибка {e}")
    if (favourites[0])  != None:
        Label(frame_root, text="Наименование", compound=LEFT, width=30, 
            justify="left", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky ="w")
        Label(frame_root, text="Символ", compound=LEFT, width=10, 
            justify="left", anchor="w").grid(row=0, column=1, padx=5, pady=5, sticky ="w")
        Label(frame_root, text="Стоимость", compound=LEFT, width=15, 
            justify="left", anchor="w").grid(row=0, column=2, padx=5, pady=5, sticky ="w")
        for i, coin in enumerate(favourites):                                  
            Label(frame_root, text=f"{coin["name"]}", compound=LEFT, width=30, 
                justify="left", anchor="w").grid(row=i+1, column=0, padx=5, pady=5, sticky ="w")
            Label(frame_root, text=f"{coin["symbol"]}", compound=LEFT, width=10, 
                justify="left", anchor="w").grid(row=i+1, column=1, padx=5, pady=5, sticky ="w")
            Label(frame_root, text=f"${coin["price_usd"]}", compound=LEFT, width=15, 
                justify="left", anchor="w").grid(row=i+1, column=2, padx=5, pady=5, sticky ="w")
    label_upd = Label(frame_footer, text=f"Последнее обновление: {time_stamp}")
    label_upd.pack(side=RIGHT, pady=5, padx=5)


def save_pickle_safely(data, filename):
    # Функция преобразует объект в байтовый поток и сериализует поток в файл с именем filename
    try:
        # Создаём директорию, если её нет
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        # Сохраняем файл
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        return True
    except (PermissionError, OSError) as e:
        return False, mb.showerror("Ошибка", f"Ошибка записи файла: {str(e)}")
    except Exception as e:
        return None, mb.showerror("Ошибка", f"Ошибка: {str(e)}")


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
        return None, mb.showerror("Информация", f"Файл {filename} не найден")  # Возвращает список (None "ok")
    except json.JSONDecodeError:
        return None, mb.showerror("Ошибка", "Ошибка декодирования JSON")   # Возвращает список (None "ok")


def load_pickle_safely(filename):
    # Функция возвращает байтовые данные из файла с именем filename
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None, mb.showerror("Информация", f"Файл {filename} не найден")  # Возвращает список (None "ok")
    except Exception as e:
        return None, mb.showerror("Ошибка", f"Ошибка: {str(e)}")


def open_modal():
    # Читаем из файла большой перечень валют и сохраняем в переменную tot_coins
    try:
        with open(total_coins_fname, 'r', encoding='utf-8') as f:
            tot_coins = json.load(f)
    except Exception as e:
            mb.showerror("Ошибка", f"При попытке открыть файл {total_coins_fname} произошла ошибка {e}.")
    
    # Создаём дочернее модальное окно с настройками.
    modal_window = Toplevel(root)
    modal_window.title("Справочник криптовалют")
    
    # Создаем фрейм
    frame_modal_w = Frame(modal_window)
    frame_modal_w.pack(fill="x", padx=10, pady=5)
    
    # Создаем заголовок
    Label(frame_modal_w, text='Название криптовалюты', compound=LEFT, 
        justify="left", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky ="w")
    Label(frame_modal_w, text='В избранное', compound=LEFT, 
        justify="left", anchor="w").grid(row=0, column=1, padx=5, pady=5, sticky ="w")

    # Восстанавливаем флаги выбранных валют
    var_chb = [BooleanVar() for _ in range(len(tot_coins))]   # Создаем пустой список-маску для отбора избранных валют
    tmp = load_json_safely(var_chb_filename)                  # Пытаемся загрузить значения из файла во временный список
    if tmp[0] is not None:                                    # Если временный список из файла прочитан, то
        for i in range(len(var_chb)):                         # Меняем значения списка var_chb на значения из
            var_chb[i].set(tmp[i])                            # временного списка

    # Создаем метки с названием криптовалюты и чекбоксы для их выбора
    for i, coin in enumerate(tot_coins):
        Label(frame_modal_w, text=f"{coin["name"]} ({coin["symbol"]})", compound=LEFT, width=20, justify="left", 
            anchor="w").grid(row=i+1, column=0, padx=5, pady=5, sticky ="w") 
        Checkbutton(frame_modal_w, variable=var_chb[i], onvalue=True, offvalue=False).grid(row=i+1, column=1, padx=5, pady=5, sticky ="w")

    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна

    # Сохраняем выбор криптовалют
    tmp1 = [value.get() for value in var_chb]    # Создаем временный список типа bool из списка var_chb
    save_json_safely(tmp1, var_chb_filename)     # Сохраняем список tmp

    # Формируем список идентификаторов избранных валют
    indices = []                            # Список для хранения идентификаторов избранных валют
    for i, value in enumerate(tot_coins):
        if var_chb[i].get():                # Если в списке на позиции i стоит True, то 
            indices.append(value["id"])     # добавляем i-й идентификатор валюты в избранное
    indices_str = ','.join(indices)         # Формируем строку для подстановки в запрос к сайту

    # Сохраняем строку для запроса информации по избранным валютам в файл
    try:
        with open(favourites_id_fname, 'w', encoding='utf-8') as f:
            f.write(indices_str)
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке сохранить файл {favourites_id_fname} произошла ошибка {e}.")

    # Обновляем избранные валюты и перерисовывам главное окно
    update_favor()


def open_modal1():
    selected_indices = set()  # Переменная для хранения списка выбранных индексом
    
    def on_select(event):
        nonlocal selected_indices  # Оъявляем переменную не локальной, доступной для изменения
        # selected_indices = set(event.widget.curselection())
        if how_to_set.get():
            selected_indices.clear
            selected_indices = set(event.widget.curselection())
        else:
            selected_indices.update(event.widget.curselection())

        
    # Читаем из файла большой перечень валют и сохраняем в переменную tot_coins
    tot_coins = load_json_safely(total_coins_fname)
    selected_indices = load_pickle_safely(SELECTED_INDS)
    # print("Old values", selected_indices)
    
    # Создаём дочернее модальное окно с настройками.
    modal_window = Toplevel(root)
    modal_window.title("Справочник криптовалют")
        
    # Создаем фреймы
    frame_btn = Frame(modal_window)
    frame_btn.pack(fill="x", padx=10, pady=5)

    frame_modal_w = Frame(modal_window)
    frame_modal_w.pack(fill="x", padx=10, pady=5)

    # Создаем переключатель "Заменить/Добавить"
    how_to_set = BooleanVar(value=True)
    Radiobutton(frame_btn, text='Заменить', variable=how_to_set, value=True).pack(side=LEFT)
    Radiobutton(frame_btn, text='Добавить', variable=how_to_set, value=False).pack(side=LEFT)

    # Создаём вертикальную Scrollbar
    scrollbar = Scrollbar(frame_modal_w, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Создаем Listbox с названием криптовалюты для их выбора
    lb = Listbox(frame_modal_w, selectmode="multiple", yscrollcommand=scrollbar.set)
    lb.pack(fill="both", expand=True)

    # Настраиваем Scrollbar, чтобы он управлял прокруткой Listbox
    scrollbar.config(command=lb.yview)

    # Заполняем Listbox элементами
    # print(tot_coins)
    # lb.insert(END, [tot_coins[i] for i in enumerate(tot_coins)])
    for i, coin in enumerate(tot_coins):
        lb.insert(END, f"{coin["name"]} ({coin["symbol"]})")
        if i in selected_indices:   # Если i совпадает с одним из элементов множества selected_indices, то
            lb.select_set(i)        # Этот элемент выделяется

    # Обработка события изменения выбора
    
    lb.bind("<<ListboxSelect>>", on_select)

    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна

    # print("Итого выбранные индексы (множество):", selected_indices)
    save_pickle_safely(selected_indices, SELECTED_INDS)







def update_favor():
    global fav_id
    global time_stamp
    global favourites_id_fname
    # Обновление избранных крниптовалют
    try:
        with open(favourites_id_fname, 'r', encoding='utf-8') as f:
            fav_id = f.read()
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке открыть файл {favourites_id_fname} произошла ошибка {e}.\nВ меню \'Настройки/Справочник\' выберите отслеживаемые валюты")
    if fav_id != '':
        data = requests.get("https://api.coinlore.net/api/ticker/", params={"id": fav_id})  # Делаем запрос к сайту по выбранным валютам
        save_json_safely(data.json(), favourites_coins_fname)
        time_stamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        try:
            with open(time_stamp_fname, 'w', encoding='utf-8') as f:
                f.write(time_stamp)
        except Exception as e:
            mb.showerror("Ошибка", f"При попытке открыть файл {time_stamp_fname} произошла ошибка {e}")
        create_labels()  # Перерисовываем виджеты главного окна. В будущем сделать обновление, а не перерисовку
    else:
        mb.showerror("Ошибка", "Не выбрано ни одной валюты")


def update_guide():
    # Обновление справочника валют
    pass


""" Основной текст программы """


# root_scr_size = [620, 520]            # начальный размер корневого окна
menu_flag = True                        # флаг видимости рамки, строки заголовка и меню окна
image = 'My_web_01.ico'
total_coins_fname ='data/total_coins.json'           # Имя файла с полным списком валют
favourites_coins_fname = 'data/indices_coins.json'   # Имя файла со справочником избранных валют
favourites_id_fname = 'data/favor_id.cfg'            # Имя файла с идентификаторами избранных валют
fav_id = ''                                          # Строка с индексами избранных валют
time_stamp = ''                                      # Текущее время
time_stamp_fname = 'data/time_update.cfg'            # Имя файла с датой и временем последнего обновления
var_chb_filename = "data/var_chb.json"               # Имя файла для флагов избранного
SELECTED_INDS = "data/selected_indices"              # Имя файла с номерами выбранных строк

# Главное окно программы
root = Tk()
root.title("Курсы криптовалют")
# root.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")
root.minsize(300, 50)  # Задал минимальный размер окна
root.iconbitmap(image)

frame_root = Frame(root, bg='gray')
frame_root.pack(fill="x", padx=10, pady=5)

frame_footer = Frame(root)
frame_footer.pack(fill="x", padx=10)

# Основное меню
menu_bar = Menu(root)
root.config(menu=menu_bar)

settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Настройки', menu=settings_menu)
settings_menu.add_command(label="Справочник", command=open_modal)
settings_menu.add_command(label="Справочник New", command=open_modal1)
settings_menu.add_separator()
settings_menu.add_command(label="Выход", command=quit)

update_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Обновление", menu=update_menu)
update_menu.add_command(label='Курсы валют', command=update_favor)
update_menu.add_command(label='Справочник валют', command=update_guide)

# Создаем виджеты в главном окне
create_labels()

# Двойной клик по окну скрывает рамку, строку заголовка и меню окна
root.bind("<Double-Button-1>", lambda event: hide_menu(event) if menu_flag else show_menu(event))

root.mainloop()