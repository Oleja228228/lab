import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
import warnings

warnings.filterwarnings('ignore')
sns.set_theme(style="whitegrid")

df = pd.read_excel('lab_4_part_5.xlsx', skiprows=1)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

df['Дата'] = pd.to_datetime(df['Дата'])
df = df.sort_values('Дата').reset_index(drop=True)

df['Прибыль'] = df['Продажи'] - df['Себестоимость']
df['Средняя_цена'] = df['Продажи'] / df['Количество']
df['Месяц_номер'] = df['Дата'].dt.month
df['Год-мес'] = df['Дата'].dt.to_period('M').astype(str)

print("Данные успешно загружены")

monthly_total = df.groupby('Год-мес', sort=False)['Продажи'].sum().reset_index()
monthly_total['Рост_спад_%'] = monthly_total['Продажи'].pct_change() * 100

plt.figure(figsize=(10, 5))
sns.barplot(
    data=monthly_total,
    x='Год-мес',
    y='Продажи',
    hue='Год-мес',
    palette='viridis',
    legend=False
)
plt.title('Динамика общего товарооборота')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 4))
plt.plot(
    monthly_total['Год-мес'],
    monthly_total['Рост_спад_%'],
    marker='o',
    linewidth=2
)
plt.axhline(0, linestyle='--')
plt.title('Ежемесячный темп роста / спада выручки (%)')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
point_sales = (
    df.groupby(['Год-мес', 'точка'], sort=False)['Продажи']
    .sum()
    .reset_index()
)

sns.lineplot(
    data=point_sales,
    x='Год-мес',
    y='Продажи',
    hue='точка',
    marker='o'
)
plt.title('Динамика продаж по точкам реализации')
plt.xticks(rotation=45)
plt.show()

brand_stats = (
    df.groupby('бренд')
    .agg({'Продажи': 'sum', 'Себестоимость': 'sum'})
    .reset_index()
)

brand_stats['Прибыль'] = brand_stats['Продажи'] - brand_stats['Себестоимость']
brand_stats['Маржа_%'] = (brand_stats['Прибыль'] / brand_stats['Продажи'] * 100).round(2)

brand_stats_melted = brand_stats.melt(
    id_vars='бренд',
    value_vars=['Продажи', 'Себестоимость']
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=brand_stats_melted,
    x='бренд',
    y='value',
    hue='variable',
    palette='muted'
)
plt.title('Объем продаж и себестоимость по брендам')
plt.show()

features = ['Месяц_номер', 'lag_1', 'lag_2']
forecast_months = 3
all_forecasts = {}

plt.figure(figsize=(12, 7))

for brand in df['бренд'].unique():

    brand_df = df[df['бренд'] == brand].set_index('Дата')

    monthly = (
        brand_df['Продажи']
        .resample('M')
        .sum()
        .to_frame()
    )

    monthly['Месяц_номер'] = monthly.index.month
    monthly['lag_1'] = monthly['Продажи'].shift(1)
    monthly['lag_2'] = monthly['Продажи'].shift(2)

    train = monthly.dropna()

    if len(train) < 6:
        continue

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    model.fit(train[features], train['Продажи'])

    history = list(monthly['Продажи'].dropna().values)
    last_date = monthly.index[-1]

    forecast_dates = []
    preds = []

    for i in range(1, forecast_months + 1):
        next_date = last_date + pd.DateOffset(months=i)
        month_num = next_date.month

        X_pred = pd.DataFrame([[
            month_num,
            history[-1],
            history[-2]
        ]], columns=features)

        pred = model.predict(X_pred)[0]
        preds.append(pred)
        forecast_dates.append(next_date)
        history.append(pred)

    all_forecasts[brand] = preds

    plt.plot(
        monthly.index,
        monthly['Продажи'],
        marker='o',
        label=f'{brand} (Факт)'
    )

    plt.plot(
        [monthly.index[-1]] + forecast_dates,
        [monthly['Продажи'].iloc[-1]] + preds,
        '--',
        marker='s',
        label=f'{brand} (Прогноз RF)'
    )

plt.title('Прогноз продаж по брендам (Random Forest)')
plt.xlabel('Дата')
plt.ylabel('Выручка')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "=" * 80)
print("ИТОГОВЫЙ АНАЛИТИЧЕСКИЙ ОТЧЕТ ПО ПРОДАЖАМ")
print("=" * 80)

total_sales = df['Продажи'].sum()
avg_monthly_growth = monthly_total['Рост_спад_%'].mean()

print("\n1. ОБЩАЯ ДИНАМИКА ПРОДАЖ")
print(f"За анализируемый период общий объем продаж составил {total_sales:,.2f} ₽.")
print(f"Средний ежемесячный темп изменения выручки: {avg_monthly_growth:.2f} %.")
print(
    "Наличие как положительных, так и отрицательных значений темпа роста "
    "свидетельствует о сезонных колебаниях спроса."
)

point_report = (
    df.groupby('точка')
    .agg({
        'Продажи': 'mean',
        'Количество': 'sum',
        'Прибыль': 'sum'
    })
    .rename(columns={'Продажи': 'Средний_чек_₽'})
    .round(2)
)

best_point = point_report['Прибыль'].idxmax()
worst_point = point_report['Прибыль'].idxmin()

print("\n2. АНАЛИЗ ТОЧЕК ПРОДАЖ")
print(point_report)
print(
    f"Наиболее эффективной точкой продаж является «{best_point}», "
    f"обеспечивающая наибольшую совокупную прибыль."
)
print(
    f"Наименее эффективной точкой является «{worst_point}», "
    "что может свидетельствовать о низком трафике или неэффективном ассортименте."
)

best_brand = brand_stats.loc[brand_stats['Маржа_%'].idxmax()]

print("\n3. АНАЛИЗ БРЕНДОВ")
print(brand_stats[['бренд', 'Продажи', 'Себестоимость', 'Прибыль', 'Маржа_%']])
print(
    f"Бренд «{best_brand['бренд']}» демонстрирует наибольшую маржинальность "
    f"({best_brand['Маржа_%']} %), что делает его приоритетным для продвижения."
)

print("\n4. ПРОГНОЗ ПРОДАЖ")
for brand, values in all_forecasts.items():
    print(f"\nБренд: {brand}")
    for i, v in enumerate(values, 1):
        print(f"  Месяц +{i}: ожидаемая выручка {v:,.2f} ₽")

