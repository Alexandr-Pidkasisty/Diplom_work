import tkinter as tk

root = tk.Tk()

# Создаём список переменных
int_var_list = [tk.IntVar() for _ in range(3)]  # 3 флажка

# Создаём и размещаем чекбоксы
for i in range(3):
    chk = tk.Checkbutton(root, variable=int_var_list[i])
    chk.pack()

# Кнопка для вывода значений
def print_values():
    values = [var.get() for var in int_var_list]
    print(values)

btn = tk.Button(root, text='Печать', command=print_values)
btn.pack()

root.mainloop()
