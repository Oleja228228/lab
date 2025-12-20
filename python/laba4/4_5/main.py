import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

file_path = "lab_4_part_5.xlsx"
xls = pd.ExcelFile(file_path)
sheet = xls.sheet_names[0]

raw = pd.read_excel(xls, sheet_name=sheet, header=None)
header_row = None
for i in range(10):
    vals = raw.iloc[i].astype(str).str.lower().tolist()
    if any("товар" in v for v in vals) and any("продаж" in v or "колич" in v for v in vals):
        header_row = i
        break
if header_row is None:
    header_row = 0

df = pd.read_excel(xls, sheet_name=sheet, header=header_row)

df.columns = [str(c).strip() for c in df.columns]
df['Дата'] = pd.to_datetime(df['Дата'], errors='coerce')
df = df.dropna(subset=['Дата']).copy()
df['month'] = df['Дата'].dt.to_period('M').dt.to_timestamp()

df['quantity'] = pd.to_numeric(df['Количество'], errors='coerce')
df['sales'] = pd.to_numeric(df['Продажи'], errors='coerce')
df['cost'] = pd.to_numeric(df['Себестоимость'], errors='coerce')
df['price'] = df['sales'] / df['quantity'].replace({0: np.nan})

monthly = (df.groupby('month')
             .agg(total_quantity=('quantity', 'sum'),
                  total_sales=('sales', 'sum'),
                  total_cost=('cost', 'sum'))
             .reset_index())
monthly['avg_price'] = monthly['total_sales'] / monthly['total_quantity'].replace({0: np.nan})
monthly['sales_mom_change'] = monthly['total_sales'].pct_change()

prod_all = (df.groupby('товар')
              .agg(total_qty=('quantity', 'sum'),
                   total_sales=('sales', 'sum'),
                   avg_price=('price', 'mean'))
              .reset_index()
              .sort_values('total_sales', ascending=False))

prod_month = (df.groupby(['month', 'товар'])
                .agg(qty=('quantity', 'sum'), sales=('sales', 'sum'))
                .reset_index())

store_all = (df.groupby('точка')
               .agg(total_qty=('quantity', 'sum'),
                    total_sales=('sales', 'sum'))
               .reset_index()
               .sort_values('total_sales', ascending=False))

store_month = (df.groupby(['month', 'точка'])
                 .agg(qty=('quantity', 'sum'), sales=('sales', 'sum'))
                 .reset_index())

horizon = 3
forecast_rows = []

for prod in prod_all['товар']:
    ts = prod_month[prod_month['товар'] == prod].sort_values('month')
    ts = ts.set_index('month').resample('M').sum().fillna(0).reset_index()
    ts['t'] = np.arange(len(ts))
    X = ts[['t']].values
    y = ts['sales'].values

    if len(ts) < 2 or np.allclose(y, 0):
        preds = [0] * horizon
    else:
        model = LinearRegression()
        model.fit(X, y)
        t_future = np.arange(len(ts), len(ts) + horizon).reshape(-1, 1)
        preds = np.maximum(model.predict(t_future), 0).tolist()

    forecast_rows.append({
        'товар': prod,
        'пред_мес_1': preds[0],
        'пред_мес_2': preds[1],
        'пред_мес_3': preds[2],
        'сумма_3мес': sum(preds)
    })

forecasts = pd.DataFrame(forecast_rows)

plt.figure(figsize=(8,4))
plt.plot(monthly['month'], monthly['total_sales'], marker='o')
plt.title('Общий товарооборот по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.grid(True)
plt.show()

top6 = prod_all.head(6)['товар']
plt.figure(figsize=(10,6))
for p in top6:
    s = prod_month[prod_month['товар']==p].set_index('month').resample('M').sum().fillna(0)['sales']
    plt.plot(s.index, s.values, marker='o', label=p)
plt.title('Динамика продаж по топ-6 товарам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.legend()
plt.grid(True)
plt.show()

top6s = store_all.head(6)['точка']
plt.figure(figsize=(10,6))
for sname in top6s:
    s = store_month[store_month['точка']==sname].set_index('month').resample('M').sum().fillna(0)['sales']
    plt.plot(s.index, s.values, marker='o', label=sname)
plt.title('Динамика продаж по топ-6 точкам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.legend()
plt.grid(True)
plt.show()

print("\nЕжемесячные итоги:\n", monthly.head())
print("\nСводка по товарам:\n", prod_all.head())
print("\nСводка по точкам:\n", store_all.head())
print("\nПрогноз продаж (3 месяца):\n", forecasts.head())
