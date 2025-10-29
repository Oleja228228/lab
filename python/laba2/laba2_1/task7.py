input_str = input("Write your string: ")

count = 1
result = ""

for i in range(1,len(input_str)):
    if input_str[i] == input_str[i-1]:
        count += 1
    else:
        result += input_str[i-1]+str(count)
        count = 1
print(result)

