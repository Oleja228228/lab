import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
import os

sns.set_theme(style="whitegrid")

FILE = "s7_data_sample_rev4_50k.xlsx"

if not os.path.exists(FILE):
    raise FileNotFoundError(f"Файл не найден: {FILE}")

df = pd.read_excel(FILE)

df["ISSUE_DATE"] = pd.to_datetime(df.get("ISSUE_DATE"), errors="coerce")
df["FLIGHT_DATE_LOC"] = pd.to_datetime(df.get("FLIGHT_DATE_LOC"), errors="coerce")

print("Информация о данных:")
print(df.info())
print("\nПример строк:")
print(df.head())

print("\n=== Описательная статистика по REVENUE_AMOUNT ===")
print(df["REVENUE_AMOUNT"].describe())

plt.figure(figsize=(8, 5))
sns.histplot(df["REVENUE_AMOUNT"].dropna(), bins=50, kde=True)
plt.title("Распределение сумм продаж (REVENUE_AMOUNT)")
plt.xlabel("Сумма продажи")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

df["Month"] = df["ISSUE_DATE"].dt.month

month_sum = df.groupby("Month", as_index=False)["REVENUE_AMOUNT"].sum().sort_values("Month")
plt.figure(figsize=(10, 5))
ax = sns.barplot(x="Month", y="REVENUE_AMOUNT", data=month_sum,
                 hue="Month", dodge=False, palette="crest")
if ax.get_legend() is not None:
    ax.get_legend().remove()
plt.title("Суммарные продажи по месяцам")
plt.xlabel("Месяц")
plt.ylabel("Сумма продаж")
plt.tight_layout()
plt.show()

top_routes = df["ORIG_CITY_CODE"].value_counts().head(10).reset_index()
top_routes.columns = ["ORIG_CITY_CODE", "count"]
plt.figure(figsize=(10, 5))
ax = sns.barplot(x="ORIG_CITY_CODE", y="count", data=top_routes,
                 hue="ORIG_CITY_CODE", dodge=False, palette="mako")
if ax.get_legend() is not None:
    ax.get_legend().remove()
plt.title("Топ-10 аэропортов отправления")
plt.xlabel("Город вылета (код)")
plt.ylabel("Количество продаж")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 6))
df["FOP_TYPE_CODE"].value_counts().plot(kind="pie", autopct="%1.1f%%", startangle=90)
plt.title("Распределение способов оплаты (FOP_TYPE_CODE)")
plt.ylabel("")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 5))
ax = sns.countplot(x="SALE_TYPE", data=df, hue="SALE_TYPE", dodge=False, palette="Set2")
if ax.get_legend() is not None:
    ax.get_legend().remove()
plt.title("Каналы продаж (ONLINE / OFFLINE)")
plt.xlabel("Тип продажи")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 5))
ax = sns.countplot(x="FFP_FLAG", data=df, hue="FFP_FLAG", dodge=False, palette="viridis")
if ax.get_legend() is not None:
    ax.get_legend().remove()
plt.title("Доля участников программы лояльности (FFP_FLAG)")
plt.xlabel("FFP_FLAG")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

daily_sales = df.groupby("ISSUE_DATE", as_index=False)["REVENUE_AMOUNT"].sum().dropna().sort_values("ISSUE_DATE")
plt.figure(figsize=(12, 5))
plt.plot(daily_sales["ISSUE_DATE"], daily_sales["REVENUE_AMOUNT"])
plt.title("Динамика продаж по дням (REVENUE_AMOUNT)")
plt.xlabel("Дата покупки")
plt.ylabel("Сумма продаж")
plt.tight_layout()
plt.show()

if len(daily_sales) > 10:
    daily_sales = daily_sales.reset_index(drop=True)
    daily_sales["day_number"] = np.arange(len(daily_sales))
    X = daily_sales[["day_number"]].values
    y = daily_sales["REVENUE_AMOUNT"].values

    model = LinearRegression()
    model.fit(X, y)

    daily_sales["predicted"] = model.predict(X)

    plt.figure(figsize=(12, 5))
    plt.plot(daily_sales["ISSUE_DATE"], daily_sales["REVENUE_AMOUNT"], label="Фактические продажи")
    plt.plot(daily_sales["ISSUE_DATE"], daily_sales["predicted"], label="Прогноз (линейный тренд)", linestyle="--")
    plt.title("Прогноз динамики продаж авиабилетов")
    plt.xlabel("Дата покупки")
    plt.ylabel("Сумма продаж")
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("Недостаточно точек в daily_sales для построения линейной модели (нужно > 10).")

print("\nАнализ успешно завершён.")
