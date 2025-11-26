numbers = []
num = input("Write your number: ")
temp = num.split()
for i in temp:
    numbers.append(float(i))

numbers.sort()
print(numbers)
print(numbers[-2])