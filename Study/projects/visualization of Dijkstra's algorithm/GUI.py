import tkinter as tk
from Algoritm import *
import numpy as np
import math
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import PhotoImage

radius = 20
width = 4
font = 'Times 10'

graph = {}
start = None  # Начальная вершина (узел 0)
finish = None  # Конечная вершина (узел 4)
path = []
distances = []

circles = []
lines = []

drawing_enabled = False  # Флаг рисования кругов
line_drawing_enabled = False  # Флаг рисования линий
delete_selected_enabled = False # Флаг удаления
is_animation_running=False# Флаг анимации

selected_circles = []  # Для хранения выбранных кругов
circle_ids = []
line_ids = []
selected_circle_ids = []

# Настройка общего стиля кнопок
button_style = {
    "padx":5,
    "pady": 5,
    "width": 30,  # Устанавливаем одинаковую ширину для всех кнопок
}
button_with_image_style = {
    "pady": 5,
    "width": 220,  # Устанавливаем одинаковую ширину для всех кнопок
}

#def draw_step_algoritm(route,vertex):
    

def run_dijkstra():

    # Удаляем связанный текст
    #draw_shapes()
    if len(graph) == 0:
        messagebox.showerror("Ошибка", "Нет ни одного ребра или граф пустой")
        return
    
    if start is None:
        messagebox.showerror("Ошибка", "Не указана стартовая вершина")
        return
    
    if finish is None:
        messagebox.showerror("Ошибка", "Не указана конечная вершина")
        return
    
    global distances, path
    path = []
    distances, previous = dijkstra(start, graph)
    path = reconstruct_path(previous, start, finish)
    print(path)
    if len(path)==0:
        messagebox.showerror("Ошибка", "путь не найден")
        return
    
    animate_path()

def adjust_coordinates(x0, y0, x1, y1):
    
    distance = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    
    adjusted_x0 = x0 + radius * (x1 - x0) / distance
    adjusted_y0 = y0 + radius * (y1 - y0) / distance
    adjusted_x1 = x1 - radius * (x1 - x0) / distance
    adjusted_y1 = y1 - radius * (y1 - y0) / distance
    
    return adjusted_x0, adjusted_y0, adjusted_x1, adjusted_y1

def animate_path():
    
    if not path or len(path) < 2:
        return  # Если путь пустой или содержит только одну точку, ничего не делать.
    
    # Начинаем анимацию с первого шага.
    animate_step(0)
    
    text_id_start = canvas.find_withtag("text_" + str(start))
    text_id_finish = canvas.find_withtag("text_" + str(finish))

    text_content_start = canvas.itemcget(text_id_start, "text")
    text_content_finish = canvas.itemcget(text_id_finish, "text")

    canvas.create_text(10, 650 ,anchor='w',text="Расстояние от вершины {} до вершины {} = {}".format(
        text_content_start, text_content_finish, distances[finish]), font='Times 20',tags="text_rez")
    path_text="Путь:"
    for i in path:
        text_id_step=canvas.find_withtag("text_" + str(i))
        path_text+=canvas.itemcget(text_id_step, "text")
        if i == finish:
            break
        path_text+="→"
        
        
    canvas.create_text(10, 680, text=path_text, font='Times 20',anchor='w',tags="text_rez")  

def animate_step(step):
    
    if not is_animation_running:
        return  # Если анимация отключена, прерываем выполнение функции

    if step < len(path) - 1:  # Проверка на диапазон
        x0, y0 = circles[circle_ids.index(path[step])]
        x1, y1 = circles[circle_ids.index(path[step + 1])]

        # Создаем линию между двумя смещенными узлами
        canvas.create_line(adjust_coordinates(x0, y0, x1, y1), width=width, fill='red', 
                           arrow="last", arrowshape=(width * 2.5, width * 5, width * 1.5), tags='animate')

        step += 1
        print(step)  # Отображаем текущее значение шага
        canvas.after(1000, animate_step, step)  # Ждем 1 секунду и переходим к следующему шагу
    else:
        # Когда последний шаг завершен, удаляем анимацию только после рендеринга всех линий
        canvas.delete("animate")
        canvas.after(1000, animate_step, 0)

def toggle_drawing():
    global delete_selected_enabled, line_drawing_enabled, drawing_enabled
    
    finish_button.config(relief=tk.RAISED)
    start_button.config(relief=tk.RAISED)

    if line_drawing_enabled:
        toggle_line_drawing()
    
    if delete_selected_enabled:
        delete_selected()
    
    drawing_enabled = not drawing_enabled
    if drawing_enabled:
        button_circles.config(relief=tk.SUNKEN)
        
        button_circles.config(text="Остановить рисование")
        canvas.bind("<Button-1>", draw_circle)  
    
    else:
        button_circles.config(text="Начать рисование")
        button_circles.config(relief=tk.RAISED)

def toggle_delete_selected():
    global delete_selected_enabled, line_drawing_enabled, drawing_enabled
    
    finish_button.config(relief=tk.RAISED)
    start_button.config(relief=tk.RAISED)

    if line_drawing_enabled:
        toggle_line_drawing()
    
    if drawing_enabled:
        toggle_drawing()
    
    delete_selected_enabled = not delete_selected_enabled
    if delete_selected_enabled:
        button_delete.config(text="Остановить удаление")
        button_delete.config(relief=tk.SUNKEN)
        
        canvas.bind("<Button-1>", delete_selected)
    
    else:
        button_delete.config(text="Удалить")
        button_delete.config(relief=tk.RAISED)
        clear_selection()

def toggle_line_drawing():
    global delete_selected_enabled, line_drawing_enabled, drawing_enabled
    
    finish_button.config(relief=tk.RAISED)
    start_button.config(relief=tk.RAISED)

    if delete_selected_enabled:
        delete_selected()
    
    if drawing_enabled:
        toggle_drawing()
    
    line_drawing_enabled = not line_drawing_enabled
    if line_drawing_enabled:
        button_line.config(text="Остановить рисование линий")
        button_line.config(relief=tk.SUNKEN)
        
        canvas.bind("<Button-1>", draw_line)
    
    else:
        button_line.config(text="Начать рисование линий")
        button_line.config(relief=tk.RAISED)
        if len(selected_circle_ids)!=0:
            for circle_id in selected_circle_ids:
                if finish==circle_id:
                    continue
                if start==circle_id:
                    canvas.itemconfig(circle_id, fill="green")
                    continue
                canvas.itemconfig(circle_id, fill="lightblue")
            selected_circle_ids.clear()
        clear_selection()

def toggle_animation():
    global is_animation_running
    is_animation_running = not is_animation_running  # Смена состояния анимации
    if is_animation_running:
        toggle_button.config(text="Остановить анимацию")
        toggle_button.config(relief=tk.SUNKEN)
        if len(path)!=0:
            animate_step(0)  # Запускаем анимацию, если она включена
    else:
        toggle_button.config(text="Запустить анимацию")
        toggle_button.config(relief=tk.RAISED)
        canvas.delete("animate")

def draw_circle(event):
    
    if drawing_enabled:
        x = event.x
        y = event.y
        if y+radius>633:
            return
        # Рисуем круг
        circle_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='lightblue')
        circle_ids.append(circle_id)
        
        # Ввод имени вершины
        while True:
            user_input = simpledialog.askstring("Input", "Название вершины:")

            # Проверка на пустой ввод
            if not user_input:
                messagebox.showwarning("Warning", "Ввод не может быть пустым. Пожалуйста, введите название вершины.")
                continue
            break
        
        text_id = canvas.create_text(x, y, text=str(user_input), font=font, tags="text_" + str(circle_id))
        
        # Сохраняем координаты в массив
        circles.append((x, y))

def calculate_text_position(x0, y0, x1, y1):
    
    # Находим среднюю точку между двумя точками
    x = (x0 + x1) / 2
    y = (y0 + y1) / 2
    
    # Вычисляем угол между двумя точками
    angle = math.atan2(y1 - y0, x1 - x0)

    # Располагаем текст на линии с учетом смещения
    text_radius_x = 2.5*width * math.cos(angle + math.pi / 2)  # Поворот на 90 градусов
    text_radius_y = 2.5*width * math.sin(angle + math.pi / 2)

    return x + text_radius_x, y + text_radius_y

def draw_line(event):
    global graph
    
    if line_drawing_enabled:
        x = event.x
        y = event.y

        for i, (cx, cy) in enumerate(circles):
            
            if (cx - radius <= x <= cx + radius) and (cy - radius <= y <= cy + radius):
                selected_circles.append((cx, cy))
                
                canvas.itemconfig(circle_ids[i], fill="red")# Подсвечиваем выбранный круг
                
                selected_circle_ids.append(circle_ids[i])  # Сохраняем ID подсвеченного круга
                
                if len(selected_circles) == 2:

                    x0, y0 = selected_circles[0]
                    x1, y1 = selected_circles[1]
                    
                    line_id = canvas.create_line(adjust_coordinates(x0, y0, x1, y1), 
                                                  width=width, fill='grey', 
                                                  arrow="last", arrowshape=(width * 2.5, width * 5, width * 1.5))
                    line_ids.append(line_id)
                    
                    while True:
                        
                        user_input = simpledialog.askstring("Input", "Вес ребра:")
                        if user_input is not None and user_input.isdigit():
                            # Добавляем ребро в граф
                            if selected_circle_ids[0] not in graph:
                                graph[selected_circle_ids[0]] = {}

                            graph[selected_circle_ids[0]][selected_circle_ids[1]] = int(user_input)
                            
                            text_id = canvas.create_text(calculate_text_position(x0, y0, x1, y1), 
                                                          text=str(user_input), font=font, 
                                                          tags="text_" + str(line_id))
                            break

                    # Убираем ранее подсвеченные круги
                    for circle_id in selected_circle_ids:
                        if finish==circle_id:
                            continue
                        if start==circle_id:
                            canvas.itemconfig(circle_id, fill="green")
                            continue
                        canvas.itemconfig(circle_id, fill="lightblue")

                    selected_circle_ids.clear()  # Очищаем список после удаления

                    clear_selection()  # Очищаем выбор для следующей операции
                break

def clear_selection():
    global selected_circles
    selected_circles = []

def is_point_near_line(x, y, line_coords, threshold=5):
    # Проверяет, находится ли точка (x, y) вблизи линии, заданной координатами line_coords.
    x1, y1, x2, y2 = line_coords
    # Вычисляем расстояние от точки до линии
    line_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
    if line_length == 0:
        return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5 < threshold

    # Вычисляем расстояние от точки до линии
    distance = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / line_length
    return distance < threshold

def delete_selected(event):
    global circles, line_ids, circle_ids, graph, radius
    
    if delete_selected_enabled:
        # Проверяем, был ли кликнут круг
        for circle_id in circle_ids:
            
            x, y = circles[circle_ids.index(circle_id)]
            
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= (radius) ** 2:  # Проверяем радиус
                
                canvas.delete(circle_id)
                circle_ids.remove(circle_id)
                circles.remove((x, y))
                
                # Удаляем связанный текст
                text_id = canvas.find_withtag("text_" + str(circle_id))
                if text_id:
                    canvas.delete(text_id[0])
                
                # Удаляем круг из графа
                if (x, y) in graph:
                    del graph[(x, y)]
                
                # Удаляем любые ребра, указывающие на этот круг
                for key in list(graph.keys()):
                    if (x, y) in graph[key]:
                        del graph[key][(x, y)]
                                
                return  # Выходим после удаления круга

        # Проверяем, была ли кликнута линия
        for line_id in line_ids:
            
            line_coords = canvas.coords(line_id)
            
            if is_point_near_line(event.x, event.y, line_coords):
                canvas.delete(line_id)
                line_ids.remove(line_id)
                
                # Удаляем связанный текст
                text_id = canvas.find_withtag("text_" + str(line_id))
                if text_id:
                    canvas.delete(text_id[0])
                
                # Находим ближайшие круги к конечным точкам линии
                start_circle = min(circles, key=lambda c: (c[0] - line_coords[0]) ** 2 + (c[1] - line_coords[1]) ** 2)
                end_circle = min(circles, key=lambda c: (c[0] - line_coords[2]) ** 2 + (c[1] - line_coords[3]) ** 2)
                
                # Удаляем линию из графа
                if start_circle in graph and end_circle in graph[start_circle]:
                    del graph[start_circle][end_circle]
                    if len(graph[start_circle]) == 0:
                        del graph[start_circle]
                
                if end_circle in graph and start_circle in graph[end_circle]:
                    del graph[end_circle][start_circle]
                    if len(graph[end_circle]) == 0:
                        del graph[end_circle]

                return

def toggle_delete_image():
    current_image = button_delete.cget("image")
    if current_image == str(delete_image):
        button_delete.config(image=delete_image_active)  # Меняем на активное изображение
    else:
        button_delete.config(image=delete_image)  # Возвращаем исходное изображение

def on_click_start(event):
    global start
    # Сохраняем предыдущую стартовую вершину для сброса ее цвета
    previous_start = start
    start = None        
    for i, (cx, cy) in enumerate(circles):
        if (cx - radius <= event.x <= cx + radius) and (cy - radius <= event.y <= cy + radius):
            # Сбрасываем цвет предыдущей стартовой вершины, если она существует
            if previous_start:
                canvas.itemconfig(previous_start, fill="lightblue")  # Сбрасываем на цвет по умолчанию

            start = circle_ids[i]
            canvas.itemconfig(circle_ids[i], fill="green") 
            canvas.unbind("<Button-1>")  # Подсвечиваем новую стартовую вершину
            start_button.config(relief=tk.RAISED)
            print(start)
            break

def on_click_finish(event):
    global finish
    # Сохраняем предыдущую конечную вершину для сброса ее цвета
    previous_finish = finish
    finish = None
    for i, (cx, cy) in enumerate(circles):
        if (cx - radius <= event.x <= cx + radius) and (cy - radius <= event.y <= cy + radius):
            # Сбрасываем цвет предыдущей конечной вершины, если она существует
            if previous_finish:
                canvas.itemconfig(previous_finish, fill="lightblue")  # Сбрасываем на цвет по умолчанию

            finish = circle_ids[i]
            if finish not in graph:
                graph[finish] = {}
            canvas.itemconfig(circle_ids[i], fill="red")  # Подсвечиваем новую конечную вершину
            canvas.unbind("<Button-1>")
            finish_button.config(relief=tk.RAISED)
            break

def select_start():
    finish_button.config(relief=tk.RAISED)

    if line_drawing_enabled:
        toggle_line_drawing()

    if delete_selected_enabled:
        delete_selected()
    
    if drawing_enabled:
        toggle_drawing()

    start_button.config(relief=tk.SUNKEN)
    canvas.bind("<Button-1>", on_click_start)

def select_finish():
    start_button.config(relief=tk.RAISED)

    if line_drawing_enabled:
        toggle_line_drawing()

    if delete_selected_enabled:
        delete_selected()
    
    if drawing_enabled:
        toggle_drawing()

    finish_button.config(relief=tk.SUNKEN)
    canvas.bind("<Button-1>", on_click_finish)

def update_parameters():
    global radius, width, font

    radius = int(entry_radius.get())
    width = int(entry_width.get())
    font = entry_font.get()

    draw_shapes()

def draw_shapes():
    global circle_ids, line_ids
    # Очистка старых фигур
    text_id = canvas.find_withtag("text_rez")
    if text_id:
        canvas.delete(text_id[0])
    for circle_id in circle_ids:
        x0,y0,x1,y1=canvas.coords(circle_id)
        radius_old=(x1-x0)/2#радиус круга
        canvas.coords(circle_id,x0 - (radius-radius_old), y0 - (radius-radius_old), x1 + (radius-radius_old), y1 + (radius-radius_old))
        text_id = canvas.find_withtag("text_" + str(circle_id))
        canvas.itemconfig(text_id[0],font=font)
    for line_id in line_ids:
        text_id = canvas.find_withtag("text_" + str(line_id))
        canvas.delete(text_id[0])
        canvas.delete(line_id)
    line_ids.clear()

    # Проходим по словарю графа и создаем линии
    for circle_id, neighbors in graph.items():
        for neighbor_id, weight in neighbors.items():
            
            x0, y0 = circles[circle_ids.index(circle_id)]  # Круг 1
            x1, y1 = circles[circle_ids.index(neighbor_id)] # Круг 2
            
            # Рисуем линию
            line_id = canvas.create_line(adjust_coordinates(x0, y0, x1, y1), 
                                                width=width, fill='grey', 
                                                arrow="last", arrowshape=(width * 2.5, width * 5, width * 1.5))
            # Добавляем к списку линий
            line_ids.append(line_id)

            text_id = canvas.create_text(calculate_text_position(x0, y0, x1, y1), 
                                                        text=str(weight), font=font, 
                                                        tags="text_" + str(line_id))
        
def close_window():
    root.destroy()  # Закрываем главное окно

def show_help():
    help_text = (
        "Инструкция по использованию программы:\n\n"
        "1. Используйте кнопку 'Начать рисование', чтобы добавить вершины на полотно.\n"
        "2. Используйте кнопку 'Начать рисование линий', чтобы соединить вершины рёбрами.\n"
        "3. Выберите стартовую и конечную вершины с помощью соответствующих кнопок.\n"
        "4. Нажмите 'Запустить алгоритм Дейкстры', чтобы найти кратчайший путь.\n"
        "5. Используйте кнопку 'Удалить', чтобы удалить вершины или рёбра.\n"
        "6. Кнопка 'Запустить/Остановить анимацию' позволяет управлять анимацией пути.\n"
        "7. Кнопка 'Закрыть окно' завершает работу программы."
    )
    messagebox.showinfo("Помощь", help_text)

# Функция для очистки канваса
def clear_canvas():
    canvas.delete("all")  # Удаляет все элементы с канваса
    canvas.create_line(-10,635,810,635,width=2)

# Инициализация основного окна
root = tk.Tk()
root.title("Визуализатор алгоритма Дейкстры")

while True:
    
    # Создание полотна для рисования
    canvas = tk.Canvas(root, width=800, height=700, bg='white')
    canvas.pack(side=tk.LEFT)

    canvas.create_line(-10,635,810,635,width=2)

    # Загрузка изображений для кнопок
    start_image = PhotoImage(file="start.png")  # Замените на путь к вашему изображению флага старта
    finish_image = PhotoImage(file="finish.png")  # Замените на путь к вашему изображению флага финиша
    vertex_image = PhotoImage(file="vertex.png")  # Замените на путь к изображению вершин
    edge_image = PhotoImage(file="edge.png")      # Замените на путь к изображению рёбер
    delete_image = PhotoImage(file="trash.png")  # Замените на путь к изображению урны
    delete_image_active = PhotoImage(file="trash2.png")  # Изображение урны при нажатии

    frame_parameters = tk.Frame(root)
    frame_parameters.pack(pady=10)

    # Поля для ввода параметров
    label_radius = tk.Label(frame_parameters, text="Размер вершин:")
    label_radius.pack(side=tk.TOP)
    entry_radius = tk.Entry(frame_parameters)
    entry_radius.insert(0, str(radius))  # Установка начального значения
    entry_radius.pack(side=tk.TOP)

    label_width = tk.Label(frame_parameters, text="Размер ребер:")
    label_width.pack(side=tk.TOP)
    entry_width = tk.Entry(frame_parameters)
    entry_width.insert(0, str(width))  # Установка начального значения
    entry_width.pack(side=tk.TOP)

    label_font = tk.Label(frame_parameters, text="Шрифт и размер текста:")
    label_font.pack(side=tk.TOP)
    entry_font = tk.Entry(frame_parameters)
    entry_font.insert(0, font)  # Установка начального значения
    entry_font.pack(side=tk.TOP)

    button_update = tk.Button(frame_parameters, text="Применить изменения", command=update_parameters, **button_style)
    button_update.pack(pady=5)

    # Создание фрейма для кнопок алгоритмов
    frame_placement = tk.Frame(root)
    frame_placement.pack(pady=10)


    # Кнопка для рисования вершин
    button_circles = tk.Button(frame_placement, text="Начать рисование", image=vertex_image, compound=tk.LEFT, command=toggle_drawing, **button_with_image_style)
    button_circles.pack()

    # Кнопка для рисования линий
    button_line = tk.Button(frame_placement, text="Начать рисование линий", image=edge_image, compound=tk.LEFT, command=toggle_line_drawing, **button_with_image_style)
    button_line.pack()

    # Кнопка для удаления объектов
    button_delete = tk.Button(frame_placement, text="Удалить", image=delete_image, compound=tk.LEFT, command=lambda: [toggle_delete_image(), toggle_delete_selected()], **button_with_image_style)
    button_delete.pack()

    # Кнопка для выбора стартовой точки
    start_button = tk.Button(frame_placement, text="Выбрать старт", image=start_image, compound=tk.LEFT, command=select_start, **button_with_image_style)
    start_button.pack()

    # Кнопка для выбора финишной точки
    finish_button = tk.Button(frame_placement, text="Выбрать финиш", image=finish_image, compound=tk.LEFT, command=select_finish, **button_with_image_style)
    finish_button.pack()
    
    # Создание фрейма для кнопок алгоритма
    frame_algoritm = tk.Frame(root)
    frame_algoritm.pack(pady=10)

    # Кнопка запуска алгоритма Дейкстры
    button = tk.Button(frame_algoritm, text="Запустить алгоритм Дейкстры", command=run_dijkstra, **button_style)
    button.pack()

    # Кнопка для запуска и остановки анимации
    toggle_button = tk.Button(frame_algoritm, text="Запустить анимацию", command=toggle_animation)
    toggle_button.pack()

    # Создание фрейма для остальных кнопок
    frame_other = tk.Frame(root)
    frame_other.pack()

    # Создание кнопки для очистки канваса
    clear_button = tk.Button(frame_other, text="Очистить все", command=clear_canvas,**button_style)
    clear_button.pack()

    # Кнопка для закрытия окна
    close_btn = tk.Button(frame_other, text="Закрыть окно", command=close_window, **button_style)
    close_btn.pack()

    # Кнопка для помощи
    button_help = tk.Button(frame_other, text="Помощь", command=show_help, **button_style)
    button_help.pack()

    # Запуск основного цикла Tkinter
    root.mainloop()