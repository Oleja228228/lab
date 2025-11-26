password = input("Write your password: ")

if len(password) < 16:
    print("Your password is too short")
elif password.isalpha() or password.isdigit():
    print("Your password is weak")
else:
    print("Your password is strong")