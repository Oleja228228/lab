numbers = []
num = input("Write your number: ")
temp = num.split()
for i in temp:
    numbers.append(float(i))

count = {}
for i in numbers:
    if i in count:
        count[i] += 1
    else:
        count[i] = 1

unique_numbers = []
for num,cnt in count.items():
    if cnt == 1:
        unique_numbers.append(num)
print(f"unique_numbers: {unique_numbers}")

repeat_numbers = []
for num,cnt in count.items():
    if cnt > 1:
        repeat_numbers.append(num)
if repeat_numbers:
    print(f"repeat_numbers: {repeat_numbers}")
else:
    print("no repeat numbers")

for i in numbers:
    if i % 2 == 0:
        print(f"even: {i}")

for i in numbers:
    if i % 2 != 0:
        print(f"odd: {i}")

for i in numbers:
    if i != int(i):
        print(f"floating point numbers: {i}")

sum_for_five = 0
for i in numbers:
    if i % 5 == 0:
        sum_for_five += i
print(f"sum of five : {sum_for_five}")

numbers.sort()
print(f"max: {numbers[-1]}")
print(f"min: {numbers[0]}")