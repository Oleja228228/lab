#елси число поделится на 5 6 7 то вывести это число в обратоном порядке в противном случае заменить все эелементы на 9

num= int(input("Write your num: "))

if num % 5 == 0 and num % 6 == 0 and num % 7 == 0:
    num = str(num)
    print(num[::-1])
else:
    num = str(num)
    for i in range(len(num)):
        num = num.replace(num[i],'9')
    print(num)
