import requests
import json

# r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":0, "limit":10})
# ass = r.json()["data"]

# with open('total_coins.json', 'w', encoding='utf-8') as f:
#             json.dump(ass, f, indent=4, ensure_ascii=False)

with open('total_coins.json', 'r', encoding='utf-8') as f:
    ass1 = json.load(f)

for coin in ass1:
    print(coin["symbol"], coin["price_usd"]) 

     
# for coin in r.json()["data"]:
#     print(coin["symbol"], coin["price_usd"])

indices = list(map(int, input("Введите индексы через пробел: ").split()))
print(indices)

filtered_r = []
# for i, value in enumerate(r.json()["data"]):
#     if i in indices:                                # Если i входит в список indices
#         print(value["symbol"], value["price_usd"])  # то печатаем
#         filtered_r.append(value)
#     else:
#         continue

for i, value in enumerate(ass1):
    if i in indices:                                # Если i входит в список indices
        print(value["symbol"], value["price_usd"])  # то печатаем
        filtered_r.append(value["id"])                # Сохраняем идентификаторы валют

print(filtered_r)
# Str = ["" + str(filtered_r[i]) +"," for i in range(len(filtered_r))]
Str = ','.join(filtered_r)
print(Str)
r1 = requests.get("https://api.coinlore.net/api/ticker/", params={"id": Str})
for coin in r1.json():
    print(coin["name"], "\t" + coin["symbol"], "\t$" + coin["price_usd"], "\t" + coin["percent_change_24h"])

# for i, value in enumerate(filtered_r):
#     print(value["symbol"], value["price_usd"])