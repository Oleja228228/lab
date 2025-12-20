#ва списка вывести новый список который состоит только общих элементов

numbers1 = []
numbers2 = []
list1 = input("Write first list: ")
list2 = input("Write second list: ")
temp1 = list1.split()
temp2 = list2.split()

for i in temp1:
    numbers1.append(int(i))

for i in temp2:
    numbers2.append(int(i))

commom_list = []

for i in numbers1:
    if i in numbers2:
        commom_list.append(i)

print(commom_list)