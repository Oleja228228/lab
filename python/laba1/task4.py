sum = int(input("Write your sum: "))
print(f"For {sum} need:")
print(f"100: {sum // 100}")
sum %= 100
print(f"50: {sum // 50}")
sum %= 50
print(f"10: {sum // 10}")
sum %= 10
print(f"5: {sum // 5}")
sum %= 5
print(f"2: {sum // 2}")
sum %= 2
print(f"1: {sum}")