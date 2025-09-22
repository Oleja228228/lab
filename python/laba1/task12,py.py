# Ввод данных от пользователя
minutes = int(input("Enter the number of minutes of conversation: "))
sms = int(input("Enter the number of SMS messages: "))
traffic_mb = int(input("Enter the amount of internet traffic (in MB): "))

base_cost = 24.99

extra_minutes_cost = max(0, (minutes - 60)) * 0.89
extra_sms_cost = max(0, (sms - 30)) * 0.59
extra_traffic_cost = max(0, (traffic_mb - 1024)) * 0.79

subtotal = base_cost + extra_minutes_cost + extra_sms_cost + extra_traffic_cost

tax = subtotal * 0.02
total = subtotal + tax

print(f"\nBasic tariff amount: {base_cost:.2f} ")
if extra_minutes_cost > 0:
    print(f"Additional minutes: {extra_minutes_cost:.2f}")
if extra_sms_cost > 0:
    print(f"Additional SMS: {extra_sms_cost:.2f}")
if extra_traffic_cost > 0:
    print(f"Additional traffic: {extra_traffic_cost:.2f}")
print(f"Налог (2%): {tax:.2f} руб.")
print(f"Total amount to be paid: {total:.2f} ")