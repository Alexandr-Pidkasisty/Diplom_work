import requests

r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":0, "limit":100})
for coin in r.json()["data"]:
    print(coin["symbol"], coin["price_usd"])