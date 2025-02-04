import csv

def center_image(matrix):
    # Инициализация временного массива 50x50 с нулями
    temp = [0] * (50 * 50)
    y_first, x_first, y_last, x_last = 28, 28, -1, -1

    # Находим границы содержимого изображения
    for y in range(28):
        for x in range(28):
            if matrix[y * 28 + x] != 0:
                if y_first > y:
                    y_first = y
                if x_first > x:
                    x_first = x
                if y_last < y:
                    y_last = y
                if x_last < x:
                    x_last = x

    # Вычисляем ширину и высоту содержимого
    width = x_last - x_first + 1
    height = y_last - y_first + 1

    # Определяем отступы для центрирования
    new_width = 50
    new_height = 50

    # Векторные отступы
    offset_x = (new_width - width) // 2
    offset_y = (new_height - height) // 2

    # Заполнениеtemp новым изображением с пропорциями
    for y in range(height):
        for x in range(width):
            temp[(offset_y + y) * new_width + (offset_x + x)] = matrix[(y_first + y) * 28 + (x_first + x)]

    return temp

with open('mnist_train.csv', 'r', newline='') as csvfile:
    with open("mnist_train_50_50_center.csv", "w", newline='') as file:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            row = list(row)
            centered_image = center_image(row[1:])  # Центрируем изображение
            writer = csv.writer(file)
            writer.writerow(centered_image)  # Записываем строку в одномерном формат
        print('конец')