a = int(input())
b = int(input())

max_sum = 0  # Максимальная сумма делителей
best_number = a  # Число с максимальной суммой делителей

# Перебираем все числа от a до b включительно
for num in range(a, b + 1):
    current_sum = 0  # Сумма делителей текущего числа
    
    # Находим все делители числа
    for divisor in range(1, num + 1):
        if num % divisor == 0:
            current_sum += divisor
    
    # Обновляем максимальную сумму и число
    if current_sum > max_sum:
        max_sum = current_sum
        best_number = num
    # Если суммы равны, выбираем большее число
    elif current_sum == max_sum and num > best_number:
        best_number = num

# Выводим результат в требуемом формате
print(best_number, max_sum)