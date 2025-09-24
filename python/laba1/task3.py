password = input("Write your password: ")
if len(password) < 16:
    print("Your password is too short")
elif (password.isdigit() == False and password.isalpha() == True) or (password.isdigit() == True and password.isalpha() == False):
    print("Your password is weak")
else:
    print("Your password is strong")