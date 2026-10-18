import requests
import json

# # Создаем и получаем ответ на запрос: большой перечень валют
# r = requests.get("https://api.coinlore.net/api/tickers/")
# coins_data = r.json()["data"]
# coins_info = r.json()["info"]

# print(f"Всего монет: {coins_info["coins_num"]}")

# # Сохраняем в файл, чтобы не делать запросы слишком часто
# with open('data_coins/total_coins.json', 'w', encoding='utf-8') as f:
#             json.dump(coins_data, f, indent=4, ensure_ascii=False)

# # Читаем из файла большой перечень валют
# with open('data_coins/total_coins.json', 'r', encoding='utf-8') as f:
#     ass = json.load(f)

# # Отладочный вывод на экран
# for coin in ass:
#     print(coin["symbol"], coin["price_usd"]) 



# Создаем и получаем ответ на запрос: большой перечень валют
r = requests.get("https://api.coinlore.net/api/assets/")
light_coins_list = r.json()["data"]

# Сохраняем в файл, чтобы не делать запросы слишком часто
with open('data_coins/assets.json', 'w', encoding='utf-8') as f:
            json.dump(light_coins_list, f, indent=4, ensure_ascii=False)

# Читаем из файла большой перечень валют
with open('data_coins/assets.json', 'r', encoding='utf-8') as f:
    ass = json.load(f)

# Отладочный вывод на экран
count = 0
for coin in ass:
    print(coin["id"], coin["symbol"], coin["name"], coin["nameid"], coin["rank"])
    count +=1
print(f"Всего {count} монет")