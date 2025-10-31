input_list = input("Write your list: ")
lst = input_list.split()

unique_list = []

for i in lst:
    if i not in unique_list:
        unique_list.append(i)
print(f"list without duplicate: {unique_list}")