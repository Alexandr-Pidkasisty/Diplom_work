import requests
import json
import threading
import time

# Получаем ответ на первый запрос
r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":0, "limit":100})
ass_data = r.json()["data"]
ass_info = r.json()["info"]["coins_num"]
count = ass_info // 100
rest = ass_info % 100
print(f"Всего монет: {ass_info}")
print(f"Число запросов: {count}")
print(f"Остаток {rest}")

# for i in range(1, count):
for i in range(1, 3):
    r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":i * 100, "limit":100})
    tmp_ass = r.json()["data"]
    ass_data = ass_data + tmp_ass
    print(f" {i}: start from {i * 100} finished")
    time.sleep(2)  # Задержка 2 сек., чтобы не перегужать сервер

if rest != 0:
    r = requests.get("https://api.coinlore.net/api/tickers/", params={"start":count, "limit":rest})
    tmp_ass = r.json()["data"]
    ass_data = ass_data + tmp_ass
    print(f" rest finished")

#print(json.dumps(ass_data, indent=4))  # Отступ в 4 пробела для читаемости

# Сортировка по имени
sorted_ass = sorted(ass_data, key=lambda x: x["name"])
# sorted_data = sorted(data, key=itemgetter('age')) # Так быстрее должно работать

# Сохраняем в файл, чтобы не делать запросы слишком часто
try:
    with open('data_coins/total_coins.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_ass, f, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Ошибка сохранения файла {e}")

# # Читаем из файла большой перечень валют
# with open('data_coins/total_coins.json', 'r', encoding='utf-8') as f:
#     ass = json.load(f)

# # Отладочный вывод на экран
# print(f"Всего монет: {len(ass)}")
# for coin in ass:
#     print(coin["name"], coin["symbol"])
