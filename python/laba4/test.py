#сгенрировать базуданных с следуюзей информацией вид фрукта масса собраного уражая количесто проданного цена за килограм, посчитаать остаток уражая сумму на которуюбыло реализовано каждого вида и посчитать процент реализации и все что считали визуализировать(на одной картинке для каждого фрукта одна картинка)
#урожай продано оставить, реализация через круговую, график суммы для всех фруктов(сделать разные виды графиков)
import pandas as pd
import matplotlib.pyplot as plt
import random

fruit_names = ["Яблоко", "Банан", "Апельсин", "Мандарин", "Персик"]
manual_prices = [3, 4, 5, 6, 7]
n = 5

data = {
    "Фрукт": fruit_names,
    "Масса урожая (кг)": [random.randint(800, 3000) for _ in range(n)],
    "Продано (кг)": [],
    "Цена за кг (руб)": manual_prices
}

for mass in data["Масса урожая (кг)"]:
    data["Продано (кг)"].append(random.randint(int(mass * 0.3), mass))

df = pd.DataFrame(data)
df["Остаток (кг)"] = df["Масса урожая (кг)"] - df["Продано (кг)"]
df["Сумма реализации (руб)"] = df["Продано (кг)"] * df["Цена за кг (руб)"]
df["% реализации"] = (df["Продано (кг)"] / df["Масса урожая (кг)"]) * 100

fig, ax = plt.subplots(figsize=(10, 5))
width = 0.4
x = range(len(df))

print(df.describe())

ax.bar(x, df["Масса урожая (кг)"], width=width, label="Масса урожая (кг)")
ax.bar([i + width for i in x], df["Продано (кг)"], width=width, label="Продано (кг)")
ax.set_xticks([i + width/2 for i in x])
ax.set_xticklabels(df["Фрукт"])
ax.set_ylabel("кг")
ax.set_title("Урожай и продано по фруктам")
ax.legend()
plt.tight_layout()
plt.show()

fig, ax1 = plt.subplots(figsize=(10, 5))

color1 = 'tab:blue'
ax1.bar(df["Фрукт"], df["Сумма реализации (руб)"], color=color1, label="Сумма реализации (руб)")
ax1.set_ylabel("Сумма реализации (руб)", color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.plot(df["Фрукт"], df["% реализации"], color=color2, marker='o', linewidth=2, label="% реализации")
ax2.set_ylabel("% реализации", color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

fig.suptitle("Сумма реализации и % реализации по фруктам")
fig.tight_layout()
plt.show()

fig, axes = plt.subplots(1, len(df), figsize=(15, 4))

for i, row in df.iterrows():
    axes[i].pie([row["Продано (кг)"], row["Остаток (кг)"]],
                labels=[f"Продано: {row['Продано (кг)']} кг", f"Остаток: {row['Остаток (кг)']} кг"],
                autopct="%1.1f%%", startangle=90)
    axes[i].set_title(row["Фрукт"])

plt.suptitle("Реализация по фруктам")
plt.tight_layout()
plt.show()

