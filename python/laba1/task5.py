num = int(input("Enter a number: "))
sum = 0
if num % 7 == 0:
    print("Magic number")
else:
    while num > 0:
        digit = num % 10
        sum += digit
        num //= 10
    print(f"Sum: {sum}")