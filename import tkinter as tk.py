import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Изначальный словарь: слова -> изображения
photo_dict = {
    "яблоко": ImageTk.PhotoImage(Image.open("images/bitcoin.png")),
    "банан": ImageTk.PhotoImage(Image.open("images/bitcoin.png")),
    "вишня": ImageTk.PhotoImage(Image.open("images/bitcoin.png"))
}

# Путь к папке с картинками
image_paths = [
    ("images/bitcoin.png", "Яблоко"),
    ("images/bitcoin.png", "Банан"),
    ("images/bitcoin.png", "Вишня")
]

# Создание основного окна
root = tk.Tk()
root.title("Словарь с изображениями")

# Виджет для выбора файла (папка)
folder_label = tk.Label(root, text="Выберите папку с изображениями:")
folder_label.pack()

folder_path = tk.StringVar()
tk.Entry(root, textvariable=folder_path).pack()

# Кнопка для выбора папки
select_button = tk.Button(root, text="Выбрать", command=lambda: select_folder(folder_path))
select_button.pack()

# Рамка для изображений
image_frame = tk.Frame(root)
image_frame.pack()

# Список для хранения виджетов-кнопок
# buttons = 

# Функция для выбора папки
def select_folder(path):
    try:
        # Получаем список файлов
        files = os.listdir(path)
        # Создаём виджеты для каждого изображения
        for i, (filename, word) in enumerate(image_paths):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                photo = ImageTk.PhotoImage(Image.open(os.path.join(path, filename)))
                # Создаём кнопку и добавляем в список
                btn = tk.Button(image_frame, image=photo, command=lambda w=photo: on_button_click(w, word))
                btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
                buttons.append(btn)
        # Обновляем метки
        label_text = tk.Label(root, text="Выберите действие:")
        label_text.pack()
        action_labels = ["Показать значение", "Открыть файл для редактирования"]
        action_labels.append(tk.Button(root, text="Выбрать действие", command=lambda w=photo, a=action_labels: on_action_click(w, a)))
        action_labels[-1].pack()
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось выбрать папку: {e}")

# Обработчики кнопок
def on_button_click(button, action="Добавить"):
    word = button.cget("text")
    photo_dict[word] = ImageTk.PhotoImage(Image.open(os.path.join(path, os.listdir(path))))
    label_text.config(text=action + ": " + word) 

def on_action_click(w, action):
    # Здесь можно добавить логику при выборе действия (например, открыть файл)
    file_path = filedialog.askopenfilename(parent=root, filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if file_path:
        try:
            photo = ImageTk.PhotoImage(Image.open(file_path))
            # Удаляем старую картинку из словаря
            if word in photo_dict:
                del photo_dict[word]
            # Добавляем новую пару
            photo_dict[word] = photo
            # Обновляем кнопку
            button.config(image=photo)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл: {e}")

# Запуск приложения
root.mainloop()