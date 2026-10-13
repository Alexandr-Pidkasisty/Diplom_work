import requests
import json

r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":0, "limit":10})
for coin in r.json()["data"]:
    print(coin["symbol"], coin["price_usd"])

indices = list(map(int, input("Введите индексы через пробел: ").split()))
print(indices)

filtered_r = []
for i, value in enumerate(r.json()["data"]):
    if i in indices:                                # Если i входит в список indices
        print(value["symbol"], value["price_usd"])  # то печатаем
        filtered_r.append(value)
    else:
        continue

print(filtered_r)

for i, value in enumerate(filtered_r):
    print(value["symbol"], value["price_usd"])