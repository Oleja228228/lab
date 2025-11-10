import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

df = pd.read_excel("s7_data_sample_rev4_50k.xlsx")

df["ISSUE_DATE"] = pd.to_datetime(df["ISSUE_DATE"], errors="coerce")
df["FLIGHT_DATE_LOC"] = pd.to_datetime(df["FLIGHT_DATE_LOC"], errors="coerce")

print(" Информация о данных:")
print(df.info())
print("\n Пример строк:")
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

plt.figure(figsize=(10, 5))
sns.barplot(x="Month", y="REVENUE_AMOUNT", data=df, estimator="sum", palette="crest")
plt.title("Суммарные продажи по месяцам")
plt.xlabel("Месяц")
plt.ylabel("Сумма продаж")
plt.tight_layout()
plt.show()

top_routes = df["ORIG_CITY_CODE"].value_counts().head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_routes.index, y=top_routes.values, palette="mako")
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
sns.countplot(x="SALE_TYPE", data=df, palette="Set2")
plt.title("Каналы продаж (ONLINE / OFFLINE)")
plt.xlabel("Тип продажи")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

plt.figure(figsize=(6, 5))
sns.countplot(x="FFP_FLAG", data=df, palette="viridis")
plt.title("Доля участников программы лояльности (FFP_FLAG)")
plt.xlabel("FFP_FLAG")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

daily_sales = df.groupby("ISSUE_DATE")["REVENUE_AMOUNT"].sum().reset_index()

plt.figure(figsize=(12, 5))
plt.plot(daily_sales["ISSUE_DATE"], daily_sales["REVENUE_AMOUNT"])
plt.title("Динамика продаж по дням (REVENUE_AMOUNT)")
plt.xlabel("Дата покупки")
plt.ylabel("Сумма продаж")
plt.tight_layout()
plt.show()

if len(daily_sales) > 10:
    daily_sales["day_number"] = np.arange(len(daily_sales))
    X = daily_sales[["day_number"]]
    y = daily_sales["REVENUE_AMOUNT"]

    model = LinearRegression()
    model.fit(X, y)

    daily_sales["predicted"] = model.predict(X)

    plt.figure(figsize=(12, 5))
    plt.plot(daily_sales["ISSUE_DATE"], daily_sales["REVENUE_AMOUNT"], label="Фактические продажи")
    plt.plot(daily_sales["ISSUE_DATE"], daily_sales["predicted"], label="Прогноз", color="red")
    plt.title("Прогноз динамики продаж авиабилетов")
    plt.xlabel("Дата покупки")
    plt.ylabel("Сумма продаж")
    plt.legend()
    plt.tight_layout()
    plt.show()

print("\n Анализ успешно завершён.")
