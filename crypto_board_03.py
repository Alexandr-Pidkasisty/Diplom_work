from tkinter import *
from tkinter import messagebox as mb
import json
import os
import requests
from datetime import datetime


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


def open_modal():
    pass


def update_favor():
    global fav_id
    global time_stamp
    # Обновление избранных крниптовалют
    try:
        with open(favourites_id_fname, 'r', encoding='utf-8') as f:
            fav_id = f.read()
    except Exception as e:
        mb.showerror("Ошибка", f"При попытке открыть файл {favourites_id_fname} произошла ошибка {e}")
        with open(favourites_id_fname, 'w', encoding='utf-8') as f:
            f.write(fav_id)
    # print(fav_id)
    data = requests.get("https://api.coinlore.net/api/ticker/", params={"id": fav_id})  # Делаем запрос к сайту по выбранным валютам
    # with open(favourites_coins_fname, 'w', encoding='utf-8') as f:
    #         json.dump(data.json(), f, indent=4, ensure_ascii=False)
    save_json_safely(data.json(), favourites_coins_fname)
    time_stamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    try:
        with open(time_stamp_fname, 'w', encoding='utf-8') as f:
            f.write(time_stamp)
    except Exception as e:
            mb.showerror("Ошибка", f"При попытке открыть файл {time_stamp_fname} произошла ошибка {e}")
    create_labels()  # Перерисовываем виджеты главного окна. В будущем сделать обновление, а не перерисовку


def update_guide():
    # Обновление справочника валют
    pass


""" Основной текст программы """


# root_scr_size = [620, 520]            # начальный размер корневого окна
menu_flag = True                        # флаг видимости рамки, строки заголовка и меню окна
image = 'My_web_01.ico'
favourites_coins_fname = 'data/indices_coins.json'   # Имя файла со справочником избранных валют
favourites_id_fname = 'data/favor_id.cfg'            # Имя файла с идентификаторами избранных валют
fav_id = '90'                                        # Строка с индексами избранных валют
time_stamp = ''                                      # Текущее время
time_stamp_fname = 'data/time_update.cfg'            # Имя файла с датой и временем последнего обновления

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