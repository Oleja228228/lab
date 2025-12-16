import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

warnings.filterwarnings('ignore')
sns.set(style="whitegrid")

try:
    df = pd.read_excel('s7_data_sample_rev4_50k.xlsx')
except FileNotFoundError:
    print("Файл данных не найден. Пожалуйста, загрузите CSV файл.")
    pass

df['ISSUE_DATE'] = pd.to_datetime(df['ISSUE_DATE'])
df['FLIGHT_DATE_LOC'] = pd.to_datetime(df['FLIGHT_DATE_LOC'])

df['REVENUE_AMOUNT'] = pd.to_numeric(df['REVENUE_AMOUNT'], errors='coerce')
df = df.dropna(subset=['REVENUE_AMOUNT'])

df['issue_month'] = df['ISSUE_DATE'].dt.month_name()
df['issue_dow'] = df['ISSUE_DATE'].dt.day_name()
df['flight_month'] = df['FLIGHT_DATE_LOC'].dt.month_name()

print("Данные успешно загружены и обработаны.")
print(f"Всего записей: {df.shape[0]}")
print("-" * 30)

print("\n--- Общие статистики ---")
print(df[['REVENUE_AMOUNT']].describe())

plt.figure(figsize=(10, 6))
sns.histplot(df['REVENUE_AMOUNT'], bins=50, kde=True, color='skyblue')
plt.title('Распределение сумм продаж (Revenue Amount)')
plt.xlabel('Сумма')
plt.ylabel('Частота')
plt.show()

top_orig = df['ORIG_CITY_CODE'].value_counts().head(10)
top_dest = df['DEST_CITY_CODE'].value_counts().head(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.barplot(x=top_orig.values, y=top_orig.index, ax=axes[0], palette='viridis')
axes[0].set_title('Топ-10 городов вылета')

sns.barplot(x=top_dest.values, y=top_dest.index, ax=axes[1], palette='magma')
axes[1].set_title('Топ-10 городов назначения')
plt.tight_layout()
plt.show()

daily_flights = df.groupby('FLIGHT_DATE_LOC').agg({
    'REVENUE_AMOUNT': 'sum',
    'ISSUE_DATE': 'count'
}).rename(columns={'ISSUE_DATE': 'FLIGHT_COUNT'})

daily_flights['Revenue_MA7'] = daily_flights['REVENUE_AMOUNT'].rolling(window=7).mean()

plt.figure(figsize=(14, 7))
plt.plot(daily_flights.index, daily_flights['REVENUE_AMOUNT'], label='Выручка (факт)', alpha=0.3)
plt.plot(daily_flights.index, daily_flights['Revenue_MA7'], label='Тренд (7 дней)', color='red', linewidth=2)
plt.title('Сезонность выручки по датам вылета')
plt.legend()
plt.show()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

pax_counts = df['PAX_TYPE'].value_counts()
axes[0].pie(pax_counts, labels=pax_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
axes[0].set_title('Распределение по типам пассажиров (AD/CHD/...)')

df['FFP_FLAG'] = df['FFP_FLAG'].fillna('No FFP')
sns.boxplot(x='FFP_FLAG', y='REVENUE_AMOUNT', data=df, ax=axes[1], showfliers=False) # showfliers=False скрывает выбросы
axes[1].set_title('Средний чек: Программа лояльности vs Обычные')
plt.show()

top_fop = df['FOP_TYPE_CODE'].value_counts().head(5).index
df_top_fop = df[df['FOP_TYPE_CODE'].isin(top_fop)]

plt.figure(figsize=(12, 6))
sns.countplot(x='FOP_TYPE_CODE', data=df_top_fop, order=top_fop, palette='Set2')
plt.title('Популярность способов оплаты (Топ-5)')
plt.show()

print("\n--- Подготовка к прогнозированию ---")

sales_ts = df.groupby('ISSUE_DATE')['REVENUE_AMOUNT'].sum().reset_index()
sales_ts = sales_ts.sort_values('ISSUE_DATE')

sales_ts['day_of_week'] = sales_ts['ISSUE_DATE'].dt.dayofweek
sales_ts['day_of_month'] = sales_ts['ISSUE_DATE'].dt.day
sales_ts['month'] = sales_ts['ISSUE_DATE'].dt.month
sales_ts['is_weekend'] = sales_ts['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

sales_ts['lag_1'] = sales_ts['REVENUE_AMOUNT'].shift(1)
sales_ts['lag_7'] = sales_ts['REVENUE_AMOUNT'].shift(7)
sales_ts['rolling_mean_7'] = sales_ts['REVENUE_AMOUNT'].shift(1).rolling(window=7).mean()

sales_ts = sales_ts.dropna()

test_days = 14
train_data = sales_ts.iloc[:-test_days]
test_data = sales_ts.iloc[-test_days:]

features = ['day_of_week', 'day_of_month', 'month', 'is_weekend', 'lag_1', 'lag_7', 'rolling_mean_7']
target = 'REVENUE_AMOUNT'

X_train = train_data[features]
y_train = train_data[target]
X_test = test_data[features]
y_test = test_data[target]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
print(f"MAE (Средняя абсолютная ошибка): {mae:.2f}")

plt.figure(figsize=(12, 6))
plt.plot(train_data['ISSUE_DATE'].iloc[-30:], train_data['REVENUE_AMOUNT'].iloc[-30:], label='История (Train)', alpha=0.5)
plt.plot(test_data['ISSUE_DATE'], y_test, label='Факт (Test)', marker='o')
plt.plot(test_data['ISSUE_DATE'], predictions, label='Прогноз (Prediction)', linestyle='--', marker='x', color='red')

plt.title(f'Прогноз объема продаж на 2 недели (Random Forest)\nMAE: {mae:.0f}')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

importances = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
print("\nВажность факторов при прогнозе:")
print(importances)