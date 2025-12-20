import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
import warnings

warnings.filterwarnings('ignore')
sns.set(style="whitegrid")

file_name = 's7_data_sample_rev4_50k.xlsx'
try:
    df = pd.read_excel(file_name)
    print(f" Данные успешно загружены из {file_name}")
except FileNotFoundError:
    print(f" Файл {file_name} не найден. Проверьте путь.")
    exit()

df['ISSUE_DATE'] = pd.to_datetime(df['ISSUE_DATE'])
df['FLIGHT_DATE_LOC'] = pd.to_datetime(df['FLIGHT_DATE_LOC'])
df['REVENUE_AMOUNT'] = pd.to_numeric(df['REVENUE_AMOUNT'], errors='coerce')
df = df.dropna(subset=['REVENUE_AMOUNT'])

df['issue_month'] = df['ISSUE_DATE'].dt.month_name()
df['issue_dow'] = df['ISSUE_DATE'].dt.day_name()

plt.figure(figsize=(10, 5))
sns.histplot(df['REVENUE_AMOUNT'], bins=50, kde=True, color='skyblue')
plt.title('Распределение сумм продаж (Revenue Amount)')
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

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
pax_counts = df['PAX_TYPE'].value_counts()
axes[0].pie(pax_counts, labels=pax_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
axes[0].set_title('Распределение по типам пассажиров')
df['FFP_FLAG'] = df['FFP_FLAG'].fillna('No FFP')
sns.boxplot(x='FFP_FLAG', y='REVENUE_AMOUNT', data=df, ax=axes[1], showfliers=False)
axes[1].set_title('Средний чек: Программа лояльности')
plt.show()

top_fop = df['FOP_TYPE_CODE'].value_counts().head(5).index
plt.figure(figsize=(10, 5))
sns.countplot(x='FOP_TYPE_CODE', data=df[df['FOP_TYPE_CODE'].isin(top_fop)], order=top_fop, palette='Set2')
plt.title('Популярность способов оплаты (Топ-5)')
plt.show()

ts_data = df.groupby('ISSUE_DATE').agg({
    'REVENUE_AMOUNT': 'sum',
    'PAX_TYPE': 'count'
}).rename(columns={'PAX_TYPE': 'FLIGHTS_COUNT'}).reset_index().sort_values('ISSUE_DATE')

def get_predictions(data, target_col):
    df_temp = data.copy()
    df_temp['day_of_week'] = df_temp['ISSUE_DATE'].dt.dayofweek
    df_temp['month'] = df_temp['ISSUE_DATE'].dt.month
    df_temp['lag_1'] = df_temp[target_col].shift(1)
    df_temp['lag_7'] = df_temp[target_col].shift(7)
    df_temp['rolling_7'] = df_temp[target_col].shift(1).rolling(window=7).mean()
    df_temp = df_temp.dropna()

    features = ['day_of_week', 'month', 'lag_1', 'lag_7', 'rolling_7']
    X = df_temp[features]
    y = df_temp[target_col]

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    last_date = df_temp['ISSUE_DATE'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=14)
    current_lags = df_temp.tail(7)[target_col].tolist()
    preds = []

    for next_date in future_dates:
        row = [[next_date.dayofweek, next_date.month, current_lags[-1], current_lags[0], np.mean(current_lags)]]
        p = model.predict(row)[0]
        preds.append(p)
        current_lags.pop(0)
        current_lags.append(p)
    return future_dates, preds

future_dates, rev_preds = get_predictions(ts_data, 'REVENUE_AMOUNT')
_, flight_preds = get_predictions(ts_data, 'FLIGHTS_COUNT')

plt.figure(figsize=(12, 6))
plt.plot(ts_data['ISSUE_DATE'].tail(21), ts_data['REVENUE_AMOUNT'].tail(21), label='История (Факт)', color='blue', marker='o')
plt.plot(future_dates, rev_preds, label='Прогноз (Выручка)', color='red', linestyle='--', marker='s')
plt.title('Прогноз ВЫРУЧКИ на 14 дней', fontsize=14)
plt.ylabel('Сумма выручки')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(ts_data['ISSUE_DATE'].tail(21), ts_data['FLIGHTS_COUNT'].tail(21), label='История (Факт)', color='green', marker='o')
plt.plot(future_dates, flight_preds, label='Прогноз (Кол-во перелетов)', color='darkorange', linestyle='--', marker='d')
plt.title('Прогноз КОЛИЧЕСТВА ПЕРЕЛЕТОВ (продаж билетов) на 14 дней', fontsize=14)
plt.ylabel('Количество проданных билетов')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


total_rev = df['REVENUE_AMOUNT'].sum()
avg_rev = df['REVENUE_AMOUNT'].mean()
top_city = top_orig.index[0]
pax_main = pax_counts.index[0]

print(f"   - Обработано записей: {len(df):,}")
print(f"   - Общая выручка в базе: {total_rev:,.2f}")
print(f"   - Средний чек (на билет): {avg_rev:.2f}")
print(f"   - Самый загруженный хаб: {top_city}")
print(f"   - Основной сегмент пассажиров: {pax_main}")

print("\n СРАВНЕНИЕ ПРОГРАММЫ ЛОЯЛЬНОСТИ (Средний чек):")
loyalty_report = df.groupby('FFP_FLAG')['REVENUE_AMOUNT'].mean()
for category, val in loyalty_report.items():
    print(f"   - {category}: {val:.2f}")
