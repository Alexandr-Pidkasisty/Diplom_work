import requests
import json
import pprint
import os
from datetime import date

def save_json_safely(data, filename):
    # Функция сериализует данные из data в файл с именем filename
    global locker
    try:
        # Создаём директорию, если её нет
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        # Сохраняем файл
        with open(filename, 'w', encoding='utf-8') as f:
          json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except TypeError as e:
        mb.showerror("Ошибка", f"Ошибка типа данных: {str(e)}")
        return False
    except (PermissionError, OSError) as e:
        mb.showerror("Ошибка", f"Ошибка записи файла: {str(e)}")
        return False


def load_json_safely(filename):
    # Функция возвращает данные из файла с именем filename
    global locker
    try:
      with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    except FileNotFoundError:
        mb.showerror("Ошибка", f"Файл {filename} не найден")  # Возвращает список (None "ok")
        return None 
    except json.JSONDecodeError:
        mb.showerror("Ошибка", "Ошибка декодирования JSON")   # Возвращает список (None "ok")
        return None 

# Query prices of one or more coins by Coin API IDs, symbols, or names
curr ='bitcoin,tether,zyncoin-2,goat-bridged-binance-bitcoin-goat' # Перечень монет ("id")
ncurr ='Bitcoin,Ethereum'                                                   # или перечень имен ("name")
auth = 'x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo'  # Ключ аутентификации
date_ = date.today().strftime("%d-%m-%Y")
print(date_)
# r = requests.get("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin&x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo")
# r = requests.get("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=bitcoin,zyncoin-2&x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo")
# r = requests.get("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + curr + "&" + auth)
# ass_data = r.json()
# save_json_safely(ass_data, 'favor_list.json')

# pprint.pprint(ass_data)

r = requests.get(f"https://api.coingecko.com/api/v3/coins/bitcoin/history?date={date_}" + "&" + auth)
ass_data = r.json()
save_json_safely(ass_data, 'btc.json')
# pprint.pprint(ass_data)
print(f'{ass_data["id"]} - {ass_data["symbol"]} - {ass_data["name"]} - {((ass_data["market_data"])["current_price"])["usd"]:.2f}')
image_link = f'{(ass_data["image"])["thumb"]}'
print(image_link)
r = requests.get(image_link)

# Полный список криптовалют/ Query all supported coins with coin ID, name and symbol
# r = requests.get("https://api.coingecko.com/api/v3/coins/list?&x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo")
# ass_data = r.json()
# save_json_safely(ass_data, 'coins_list.json')

# Query all supported currencies on CoinGecko
# r = requests.get("https://api.coingecko.com/api/v3/simple/supported_vs_currencies?&x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo")
# ass_data = r.json()
# pprint.pprint(ass_data)

# Query all supported coin categories on CoinGecko
# r = requests.get("https://api.coingecko.com/api/v3/coins/categories/list?&x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo")
# ass_data = r.json()
# pprint.pprint(ass_data)

# Query all supported exchanges with ID and name
# r = requests.get("https://api.coingecko.com/api/v3/exchanges/list?&x_cg_demo_api_key=CG-CzGaZZtQp9cyNQy8rsT1sJNo")
# ass_data = r.json()
# pprint.pprint(ass_data)