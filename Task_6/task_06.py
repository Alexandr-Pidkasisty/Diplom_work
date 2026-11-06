import requests
import json
from datetime import date
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import messagebox as mb


def response(*args, **kwargs):
    # Формирует запрос к серверу и возвращает данные в формате JSON.
    try:
        r = requests.get(*args, **kwargs)   # Формируем запрос и получаем данные
        r.raise_for_status()                # выбросит HTTPError для кодов 4xx/5xx
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


def load_image(url):
    # Скачивает картинку
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        image_data = BytesIO(resp.content)
        img = Image.open(image_data)
        img.thumbnail((600, 480), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as er:
        mb.showerror("Ошибка", f'При загрузке изображения получена ошибка {er}')
        return None


def cmb_names_on_select(event):
    # Обработка события выбора в виджете cmb_names
    get_data()


def get_data():
    # Получение данных и вывод информации на дашборд
    name = cmb_names_var.get()
    id = COINS[name]
    date_ = date.today().strftime("%d-%m-%Y")
    r = response(f"https://api.coingecko.com/api/v3/coins/{id}/history?date={date_}" + "&" + AUTH_KEY)
    ass_data = r.json()
    image_link = f'{(ass_data["image"])["small"]}'
    img = load_image(image_link)
    if img:
        l_image.configure(image=img)
        l_image.image = img
    l_name.configure(text=ass_data["name"], font=FONT, width=len(ass_data["name"])+2)
    l_simbol.configure(text=ass_data["symbol"], font=FONT, width=len(ass_data["symbol"])+2)
    l_price.configure(text=f'${((ass_data["market_data"])["current_price"])["usd"]:.2f}', font=FONT, 
                      width=len(f'{((ass_data["market_data"])["current_price"])["usd"]:.2f}')+3)


""" Основной текст программы """

AUTH_KEY = 'x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo'  # Ключ аутентификации
MAIN_ICON = 'My_web_01.ico'                                 # Имя файла с иконкой программы
# Популярные криптовалюты
COINS_NAME = ["Bitcoin", "Ethereum", "Tether", "BNB", "XRP", "USDC", "Solana", "TRON", "Figure Heloc", "Zcash"] 
COINS = {"Bitcoin": "bitcoin", "Ethereum": "ethereum", "Tether": "tether", "BNB":"binancecoin", "XRP": "ripple",
         "USDC": "usd-coin", "Solana": "solana", "TRON": "tron", "Figure Heloc": "figure-heloc", "Zcash": "zcash"}

FONT = ("Arial", 12)

root = Tk()
root.title("Курсы популярных криптовалют")
root.minsize(350, 50)       # Задал минимальный размер окна
root.iconbitmap(MAIN_ICON)  # Задал иконку приложения

frame_root = Frame(root)
frame_root.pack(fill="x", padx=5, pady=5)
frame_info = Frame(root)
frame_info.pack(fill="x", padx=5, pady=5)

Label(frame_root, text='Выберите криптовалюту').pack(side=LEFT, padx=5, pady=5)

cmb_names_var = StringVar()
cmb_names = ttk.Combobox(frame_root, textvariable=cmb_names_var, values=COINS_NAME, state="readonly")
cmb_names.pack(side=LEFT)
cmb_names.bind("<<ComboboxSelected>>", cmb_names_on_select)

# Вывод заголовков на дашборд
frame_info.columnconfigure(3, weight=1)  # Столбец 3 будет растягиваться
Label(frame_info, text="Наименование").grid(row=0, column=1, padx=(5,0), pady=5, sticky ="w")
Label(frame_info, text="Символ").grid(row=0, column=2, padx=(5,0), pady=5, sticky ="w")
Label(frame_info, text="Стоимость").grid(row=0, column=3, padx=5, pady=5, sticky ="e")

# Вывод информации на дашборд
l_image = Label(frame_info, text="")
l_image.grid(row=1, column=0, padx=(5,0), pady=5, sticky ="w")
l_name = Label(frame_info, text="", compound=LEFT, width=20, 
    justify="left", anchor="w")
l_name.grid(row=1, column=1, padx=(5,0), pady=5, sticky ="w")
l_simbol = Label(frame_info, text="", compound=LEFT, width=15, 
    justify="left", anchor="w")
l_simbol.grid(row=1, column=2, padx=(5,0), pady=5, sticky ="w")
l_price = Label(frame_info, text="", compound=LEFT, width=25, 
    justify="left", anchor="e")
l_price.grid(row=1, column=3, padx=5, pady=5, sticky ="e")

# Выбор криптовалюты по умолчанию и ее отображение
cmb_names_var.set(COINS_NAME[0])
get_data()

root.mainloop()
