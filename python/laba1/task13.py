import random

random_number = random.randint(1, 100)

while True:
    num = int(input("Write your number: "))
    if num > random_number:
        print("Your number is greater.")
    elif num < random_number:
        print("Your number is lower.")
    else:
        print("You guessed it")
        break