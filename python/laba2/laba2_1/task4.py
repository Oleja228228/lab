numbers1 = []
num = input("Write your number for first list: ")
temp = num.split()
for i in temp:
    numbers1.append(float(i))

numbers2 = []
num = input("Write your number for second list: ")
temp = num.split()
for i in temp:
    numbers2.append(float(i))

lenght = len(numbers1) if len(numbers1)  < len(numbers2) else len(numbers2)
print(lenght)

commom_element = list(set(numbers1) & set(numbers2))
print(f"present in both sets: {commom_element}")

only_in_first = list(set(numbers1) - set(numbers2))
print(f"only in first: {only_in_first}")

only_in_second = list(set(numbers2) - set(numbers1))
print(f"only in second: {only_in_second}")

diff_element = list(set(numbers1) ^ set(numbers2))
print(f"without both element: {diff_element}")