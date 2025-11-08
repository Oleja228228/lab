import numpy as np

n = int(input("Введите количество участков дороги: "))

lengths = np.array(list(map(float, input("Введите длины участков (через пробел): ").split())))
speeds = np.array(list(map(float, input("Введите средние скорости на участках (через пробел): ").split())))

k = int(input("Введите номер участка, на котором автомобиль въехал на дорогу: "))
p = int(input("Введите номер участка, после которого выехал: "))

if not (1 <= k <= n and 1 <= p <= n and k <= p):
    print("Ошибка: номера участков введены некорректно.")
else:
    L = lengths[k-1:p]
    V = speeds[k-1:p]

    total_distance = np.sum(L)
    total_time = np.sum(L / V)
    average_speed = total_distance / total_time

    print(f"Длина пути: {total_distance:.2f} км")
    print(f"Время в пути: {total_time:.2f} ч")
    print(f"Средняя скорость: {average_speed:.2f} км/ч")
