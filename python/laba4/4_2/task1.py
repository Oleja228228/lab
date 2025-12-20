import numpy as np

expenses = np.array([150, 170, 160, 140, 130, 200, 220, 210, 180, 160, 155, 165])

winter = expenses[[11, 0, 1]].sum()
summer = expenses[[5, 6, 7]].sum()

print(f"Зимние расходы: {winter}")
print(f"Летние расходы: {summer}")

if winter > summer:
    print("Больше тратится зимой.")
elif summer > winter:
    print("Больше тратится летом.")
else:
    print("Расходы одинаковые.")

max_value = expenses.max()
max_months = np.where(expenses == max_value)[0] + 1
print(f"Наибольшие расходы были в месяцах: {max_months}")
