""" Графический редактор """
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from PIL import Image, ImageTk, ImageGrab

pen_color = "black"

def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(x, y, x + 5, y + 5, fill=pen_color, outline=pen_color)

def load_image():
    try:
        file_path = fd.askopenfilename(filetypes=[("Image files", "*.png; *.jpg; *.jpeg; *bmp; *.gif; *.webp")])  # Открываем файлы заданных типов
        if file_path:  # Если имя не пустое
            image = Image.open(file_path)           # Открываем картинку
            image = image.resize((600, 400))        # Подгоняем ее размер под окно
            image_tk = ImageTk.PhotoImage(image)    # Преобразовываем изображение в такое, какое можно вывести на метку
            canvas.create_image(0, 0, anchor=NW, image=image_tk)  # Выводим на полотно, привязываем к северо-западному углу
            canvas.image = image_tk                 # Сохраняем изображение
    except Exception as e:
        mb.showerror("Ошибка", f"Не удалось загрузить файл из-за ошибки {e}")


def save_image():
    try:
        file_path = fd.asksaveasfilename(defaultextension='*.png', filetypes=[('PNG files', '*.png')])  # Сохраняем в файл типа png
        if file_path:
            x = window.winfo_rootx() # Определяем x- координату верхнего левого угла рисунка
            y = window.winfo_rooty() # Определяем y- координату верхнего левого угла рисунка
            x1 = x + 600             # Определяем x- координату нижнего правого угла рисунка
            y1 = y + 400             # Определяем y- координату нижнего правого угла рисунка
            ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)  # Считываем картинку, обрезаем лишнее и сохраняем
            mb.showinfo("Сохранено", "Изображение успешно сохранено")
    except Exception as e:
        mb.showerror("Обшибка", f"Не удалось сохранить файл из-за ошибки {e}")


def quit_prg():
    window.destroy()

window = Tk()
window.title("Графический редактор")

canvas = Canvas(width=600, height=400)
canvas.pack()
canvas.bind("<B1-Motion>", draw)  # Событие, которое срабатывает, когда пользователь двигает мышь с зажатой левой кнопкой

colors = ["red", "green", "blue", "black", "yellow", "gray"]

# Создаем метки для выбора цвета
for color in colors:
    lbl = Label(bg=color, width=8, height=2)
    lbl.pack(side=LEFT)
    lbl.bind("<Button-1>", lambda e, c=color: globals().update(pen_color=c))  # Клик левой кнопкой мыши
    # globals возвращает все глобальные переменные, а функция update изменяет выбранные переменные

# Button(text="Загрузить", command=load_image).pack()
# Button(text="Сохранить", command=save_image).pack()

menu_bar = Menu(window)
window.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Файл', menu=file_menu)
file_menu.add_command(label='загрузить изображение', command=load_image)
file_menu.add_command(label='Сохранить изображение', command=save_image)
file_menu.add_separator()
file_menu.add_command(label='Выход', command=quit_prg)

window.mainloop()
