#Если длинна строки нечетное число и строка состоит только из цифр найти частно от деления на 7 если тоьлко из букви и нечетная заменить a на о в проотивном члучае вывести каждый второй элемент
text = input("Write your text: ")
length = len(text)
if length % 2 != 0 and text.isdigit():
    print(int(text) / 7)
elif length % 2 != 0 and text.isdigit() == False:
    print(text.replace("o", "a"))
else:
    print(text[1::2])
