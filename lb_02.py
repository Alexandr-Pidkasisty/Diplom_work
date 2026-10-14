import tkinter as tk

root = tk.Tk()
listbox = tk.Listbox(root, selectmode="multiple")
listbox.pack()

# Добавляем элементы в список
for i in range(5):
    listbox.insert(tk.END, f"Элемент {i}")

def on_select(event):
    print("on_select working!")
    # Получаем индексы выделенных элементов
    selected_indices = listbox.curselection()
    
    # Преобразуем строки в integers (если нужно) и получаем сами элементы
    selected_items = [listbox.get(i) for i in selected_indices]
    
    print("Выбранные индексы:", selected_indices)
    print("Выбранные элементы:", selected_items)

# Привязываем функцию к событию изменения выбора
listbox.bind("<<ListboxSelect>>", on_select)

root.mainloop()
