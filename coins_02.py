import requests
import json

# Получаем ответ на запрос: большой перечень валют
# r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":0, "limit":10})
# ass = r.json()["data"]

# Сохраняем в файл, чтобы не делать запросы слишком часто
# with open('total_coins.json', 'w', encoding='utf-8') as f:
#             json.dump(ass, f, indent=4, ensure_ascii=False)

# Читаем из файла большой перечень валют
with open('total_coins.json', 'r', encoding='utf-8') as f:
    ass1 = json.load(f)

# Отладочный вывод на экран
for coin in ass1:
    print(coin["symbol"], coin["price_usd"]) 

# for coin in r.json()["data"]:
#     print(coin["symbol"], coin["price_usd"])

# Аналог Listbox с выбором индексов.
indices = list(map(int, input("Введите индексы через пробел: ").split()))
print(indices)      # Отладочный вывод на экран

filtered_r = []     # Переменная для хранения идентификаторов выбранных валют
# for i, value in enumerate(r.json()["data"]):
#     if i in indices:                                  # Если i входит в список indices
#         print(value["symbol"], value["price_usd"])    # то печатаем
#         filtered_r.append(value)
#     else:
#         continue

# Формируем список с идентификаторами выбранных валют
for i, value in enumerate(ass1):
    if i in indices:                                    # Если i входит в список indices
        print(value["symbol"], value["price_usd"])      # то выводим на экран контрольную информацию
        filtered_r.append(value["id"])                  # и сохраняем идентификаторы валют

print(filtered_r)                                       # Отладочный вывод на экран

Str = ','.join(filtered_r)                              # Формируем строку для подстановки в запрос к сайту
print(Str)
r1 = requests.get("https://api.coinlore.net/api/ticker/", params={"id": Str})  # Делаем запрос к сайту по выбранным валютам
for coin in r1.json():                                  # Контрольный вывод на экран результатов запроса
    print(coin["name"], "\t" + coin["symbol"], "\t$" + coin["price_usd"], "\t" + coin["percent_change_24h"])

# for i, value in enumerate(filtered_r):
#     print(value["symbol"], value["price_usd"])