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
    global FAVOURITES_COINS_FNAME
    global time_stamp
    clear_frame_root()  # Очищаем главное окно от виджетов
    favourites = load_json_safely(FAVOURITES_COINS_FNAME)
    try:
        with open(TIME_STAMP_FNAME, 'r', encoding='utf-8') as f:
            time_stamp = f.read()
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке открыть файл {TIME_STAMP_FNAME} произошла ошибка {e}")
    if (favourites[0])  != None:
        Label(frame_root, text="Наименование", compound=LEFT, width=30, 
            justify="left", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky ="w")
        Label(frame_root, text="Символ", compound=LEFT, width=10, 
            justify="left", anchor="w").grid(row=0, column=1, padx=5, pady=5, sticky ="w")
        Label(frame_root, text="Стоимость", compound=LEFT, width=15, 
            justify="left", anchor="e").grid(row=0, column=2, padx=5, pady=5, sticky ="w")
        for i, coin in enumerate(favourites):                                  
            Label(frame_root, text=f"{coin["name"]}", compound=LEFT, width=30, 
                justify="left", anchor="w").grid(row=i+1, column=0, padx=5, pady=5, sticky ="w")
            Label(frame_root, text=f"{coin["symbol"]}", compound=LEFT, width=10, 
                justify="left", anchor="w").grid(row=i+1, column=1, padx=5, pady=5, sticky ="w")
            Label(frame_root, text=f"${coin["price_usd"]}", compound=LEFT, width=15, 
                justify="left", anchor="e").grid(row=i+1, column=2, padx=5, pady=5, sticky ="w")
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
    selected_indices = set()  # Множество для хранения списка выбранных индексом
    sel_buffer = []           # Буфер для хранения списка выделенных элементов виджета lb
    sel_ind_flag = False      # Флаг отображения выбранных индексов при открытии окна modal_window

    def chk_btn_changed():
        nonlocal sel_ind_flag
        print(chk_btn_var.get())
        sel_ind_flag = chk_btn_var.get()
        
    def on_select(event):
        # Функция устанавливает новые значения для множества selected_indices
        nonlocal selected_indices  # Оъявляем переменную не локальной, доступной для изменения
        # selected_indices = set(event.widget.curselection())
        if how_to_set.get():
            selected_indices.update(event.widget.curselection())
        else:
            selected_indices.clear
            selected_indices = set(event.widget.curselection())


    def on_select1(event):
        # Функция сохраняет список выделенных элементов виджета lb в буфере
        nonlocal sel_buffer
        sel_buffer = event.widget.curselection()

    def on_click():
        # Функция устанавливает новые значения для множества selected_indices
        # и завершает работу окна
        nonlocal selected_indices  # Оъявляем переменную не локальной, доступной для изменения
        nonlocal sel_buffer
        if how_to_set.get():
            selected_indices.update(sel_buffer)     # добавляем
        else:
            selected_indices.clear
            selected_indices = set(sel_buffer)      # заменяем
        modal_window.destroy()

    # Читаем из файла большой перечень валют и сохраняем в переменную tot_coins
    tot_coins = load_json_safely(TOTAL_COINS_FNAME)
    selected_indices = load_pickle_safely(SELECTED_INDS)

    # Читаем из файла флаг
    sel_ind_flag = load_pickle_safely("data/sel_ind_flag.cfg")
    print("To read", sel_ind_flag)
    
    # Создаём дочернее модальное окно с настройками.
    modal_window = Toplevel(root)
    modal_window.title("Выбор монет")
        
    # Создаем фреймы
    frame_lab = Frame(modal_window)
    frame_lab.pack(fill="x", padx=10, pady=5)
    frame_rbtn = Frame(modal_window)
    frame_rbtn.pack(fill="x", padx=10, pady=5)
    frame_modal_w = Frame(modal_window)
    frame_modal_w.pack(fill="x", padx=10, pady=5)
    frame_buttons = Frame(modal_window)
    frame_buttons.pack(fill="x", padx=10, pady=5)

    # Создаем метку с общим числом монет
    Label(frame_lab, text=f"Общее число монет в справочнике: {len(tot_coins)}").pack(side=LEFT)

    # Создаем переключатель "Заменить/Добавить"
    how_to_set = BooleanVar(value=True)
    Radiobutton(frame_rbtn, text='Добавить', variable=how_to_set, value=True).pack(side=LEFT)
    Radiobutton(frame_rbtn, text='Заменить', variable=how_to_set, value=False).pack(side=LEFT)

    # Создаём вертикальную Scrollbar
    scrollbar = Scrollbar(frame_modal_w, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Создаем Listbox с названием криптовалюты для их выбора
    lb = Listbox(frame_modal_w, selectmode="multiple", yscrollcommand=scrollbar.set)
    lb.pack(fill="both", expand=True)

    # Настраиваем Scrollbar, чтобы он управлял прокруткой Listbox
    scrollbar.config(command=lb.yview)

    # Заполняем Listbox элементами
    indices = []                                    # Список для хранения идентификаторов избранных валют
    for i, coin in enumerate(tot_coins):
        lb.insert(END, f"{coin["name"]} ({coin["symbol"]})")
        if sel_ind_flag and i in selected_indices:  # Если i совпадает с одним из элементов множества selected_indices, то
            lb.select_set(i)                        # Этот элемент выделяется

    # Обработка события изменения выбора элементов lb
    lb.bind("<<ListboxSelect>>", on_select1)

    chk_btn_var = BooleanVar(value=sel_ind_flag)
    chk_btn = Checkbutton(frame_modal_w, text="Выделять избранные монеты при последующем открытии окна", variable=chk_btn_var,
                          onvalue=True, offvalue=False, command=chk_btn_changed)
    chk_btn.pack(side=LEFT, padx=5)
    # chk_btn.deselect()

    btn_save = Button(frame_buttons, text="Сохранить и выйти", command=on_click)
    btn_save.pack(side=LEFT)

    # Настраиваем модальность
    modal_window.transient(root)    # Связываем с главным окном
    modal_window.grab_set()         # Захватываем ввод
    modal_window.focus_set()        # Переводим фокус на окно
    modal_window.wait_window()      # Ждём закрытия окна

    # Сохраняем множество со списком выбранных индексов
    save_pickle_safely(selected_indices, SELECTED_INDS)

    # Сохраняем выбор "Выделять избранные монеты при последующем открытии окна"
    save_pickle_safely(sel_ind_flag, "data/sel_ind_flag.cfg")
    print("saved", sel_ind_flag)

    # Формируем список идентификаторов избранных валют
    for i, coin in enumerate(tot_coins):
        if i in selected_indices:           # Если i совпадает с одним из элементов множества selected_indices, то
            indices.append(coin["id"])      # добавляем i-й идентификатор валюты в избранное
    indices_str = ','.join(indices)         # Формируем строку для подстановки в запрос к сайту

    # Сохраняем строку для запроса информации по избранным валютам в файл
    try:
        with open(FAVOURITES_ID_FNAME, 'w', encoding='utf-8') as f:
            f.write(indices_str)
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке сохранить файл {FAVOURITES_ID_FNAME} произошла ошибка {e}.")
    
    # Обновляем избранные валюты и перерисовывам главное окно
    update_favor()

# def open_modal1
    

def update_favor():
    global fav_id
    global time_stamp
    global FAVOURITES_ID_FNAME
    # Обновление избранных крниптовалют
    try:
        with open(FAVOURITES_ID_FNAME, 'r', encoding='utf-8') as f:
            fav_id = f.read()
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке открыть файл {FAVOURITES_ID_FNAME} произошла ошибка {e}.\nВ меню \'Настройки/Справочник\' выберите отслеживаемые валюты")
    if fav_id != '':
        # data = requests.get("https://api.coinlore.net/api/ticker/", params={"id": fav_id})  # Делаем запрос к сайту по выбранным валютам
        data = response(FAVOURITES_COINS, {"id": fav_id}, (10, 30)) # Делаем запрос к сайту по выбранным валютам
        save_json_safely(data.json(), FAVOURITES_COINS_FNAME)
        time_stamp = datetime.now().strftime("%d.%m.%Y %H:%M")
        try:
            with open(TIME_STAMP_FNAME, 'w', encoding='utf-8') as f:
                f.write(time_stamp)
        except Exception as e:
            mb.showerror("Ошибка", f"При попытке открыть файл {TIME_STAMP_FNAME} произошла ошибка {e}")
        create_labels()  # Перерисовываем виджеты главного окна. В будущем сделать обновление, а не перерисовку
    else:
        mb.showerror("Ошибка", "Не выбрано ни одной валюты")


def update_guide():
    # Обновление справочника валют
    pass


def response(url, prm, tm):
    # Формирует запрос к серверу и возвращает данные в формате JSON. Параметры: url - адрес сервера,
    # prm - параметры запроса, tm - кортеж с максимальным временем ожидания соединения с сервером и
    # максимальным временем ожидания получения данных
    try:
        r = requests.get(url, params=prm, timeout=tm)   # Формируем запрос и получаем данные
        r.raise_for_status()                            # выбросит HTTPError для кодов 4xx/5xx
        return r
    except requests.Timeout:
        mb.showerror("Ошибка", "Запрос превысил время ожидания")
        return None
    except requests.ConnectionError:
        mb.showerror("Ошибка", "Не удалось соединиться с сервером")
        return None
    except requests.HTTPError as e:
        mb.showerror(f"HTTP-ошибка: {e.r.status_code}")
        return None
    except requests.RequestException as e:
        # Сюда попадут любые другие ошибки requests
        mb.showerror(f"Произошла ошибка при запросе: {e}")
        return None


""" Основной текст программы """


# root_scr_size = [620, 520]            # начальный размер корневого окна
menu_flag = True                        # флаг видимости рамки, строки заголовка и меню окна
MAIN_ICON = 'My_web_01.ico'
TOTAL_COINS_FNAME ='data/total_coins.json'           # Имя файла с полным списком валют
FAVOURITES_COINS_FNAME = 'data/indices_coins.json'   # Имя файла со справочником избранных валют
FAVOURITES_ID_FNAME = 'data/favor_id.cfg'            # Имя файла с идентификаторами избранных валют
TIME_STAMP_FNAME = 'data/time_update.cfg'            # Имя файла с датой и временем последнего обновления
var_chb_filename = "data/var_chb.json"               # Имя файла для флагов избранного
SELECTED_INDS = "data/selected_indices.cfg"          # Имя файла с номерами выбранных строк
REQUEST_TOTAL_COINS ="https://api.coinlore.net/api/tickers/"    # Адрес запроса для всех монет
FAVOURITES_COINS = "https://api.coinlore.net/api/ticker/"       # Адрес запроса по выбранным монетам     

fav_id = ''                                          # Строка с индексами избранных валют
time_stamp = ''                                      # Текущее время

# Главное окно программы
root = Tk()
root.title("Курсы криптовалют")
# root.geometry(f"{root_scr_size[0]}x{root_scr_size[1]}")
root.minsize(300, 50)  # Задал минимальный размер окна
root.iconbitmap(MAIN_ICON)

frame_root = Frame(root, bg='gray')
frame_root.pack(fill="x", padx=10, pady=5)

frame_footer = Frame(root)
frame_footer.pack(fill="x", padx=10)

# Основное меню
menu_bar = Menu(root)
root.config(menu=menu_bar)

settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Настройки', menu=settings_menu)
settings_menu.add_command(label="Выбрать монеты", command=open_modal)
settings_menu.add_separator()
settings_menu.add_command(label="Выход", command=quit)

update_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Обновление", menu=update_menu)
update_menu.add_command(label='Избранное', command=update_favor)
update_menu.add_command(label='Справочник монет', command=update_guide)

# Создаем виджеты в главном окне
create_labels()

# Двойной клик по окну скрывает рамку, строку заголовка и меню окна
root.bind("<Double-Button-1>", lambda event: hide_menu(event) if menu_flag else show_menu(event))

root.mainloop()