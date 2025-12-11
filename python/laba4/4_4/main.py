import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")

FILE = "s7_data_sample_rev4_50k.xlsx"

if not os.path.exists(FILE):
    raise FileNotFoundError(f"Файл не найден: {FILE}")

df = pd.read_excel(FILE)

# ===================== ПОДГОТОВКА ДАННЫХ =====================
df["ISSUE_DATE"] = pd.to_datetime(df["ISSUE_DATE"], errors="coerce")
df["FLIGHT_DATE_LOC"] = pd.to_datetime(df["FLIGHT_DATE_LOC"], errors="coerce")

print("Информация о данных:")
print(df.info())

print("\nПример строк:")
print(df.head())

print("\n=== Описательная статистика по REVENUE_AMOUNT ===")
print(df["REVENUE_AMOUNT"].describe())

# ---------------------- Гистограмма продаж ----------------------
plt.figure(figsize=(8, 5))
sns.histplot(df["REVENUE_AMOUNT"].dropna(), bins=50, kde=True)
plt.title("Распределение сумм продаж (REVENUE_AMOUNT)")
plt.xlabel("Сумма продажи")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

# ---------------------- Доп. признаки ----------------------
df["Month"] = df["ISSUE_DATE"].dt.month
month_sum = df.groupby("Month", as_index=False)["REVENUE_AMOUNT"].sum()

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

# ---------------------- Топ направлений ----------------------
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

# ---------------------- Способы оплаты ----------------------
plt.figure(figsize=(6, 6))
df["FOP_TYPE_CODE"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Распределение способов оплаты (FOP_TYPE_CODE)")
plt.ylabel("")
plt.tight_layout()
plt.show()

# ---------------------- Каналы продаж ----------------------
plt.figure(figsize=(6, 5))
ax = sns.countplot(x="SALE_TYPE", data=df, hue="SALE_TYPE", dodge=False, palette="Set2")
if ax.get_legend() is not None:
    ax.get_legend().remove()
plt.title("Каналы продаж (ONLINE / OFFLINE)")
plt.xlabel("Тип продажи")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

# ---------------------- Участие в FFP ----------------------
plt.figure(figsize=(6, 5))
ax = sns.countplot(x="FFP_FLAG", data=df, hue="FFP_FLAG", dodge=False, palette="viridis")
if ax.get_legend() is not None:
    ax.get_legend().remove()
plt.title("Доля участников программы лояльности (FFP_FLAG)")
plt.xlabel("FFP_FLAG")
plt.ylabel("Количество билетов")
plt.tight_layout()
plt.show()

# ---------------------- Динамика продаж ----------------------
daily_sales = df.groupby("ISSUE_DATE", as_index=False)["REVENUE_AMOUNT"].sum().dropna()
daily_sales = daily_sales.sort_values("ISSUE_DATE")

plt.figure(figsize=(12, 5))
plt.plot(daily_sales["ISSUE_DATE"], daily_sales["REVENUE_AMOUNT"])
plt.title("Динамика продаж по дням (REVENUE_AMOUNT)")
plt.xlabel("Дата")
plt.ylabel("Сумма продаж")
plt.tight_layout()
plt.show()

# ======================= УСТОЙЧИВЫЙ ПРОГНОЗ: HOLT-WINTERS с защитой от отрицательных значений =======================
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

print("\nСтрою устойчивый прогноз Holt-Winters (с защитой от отрицаний)...")

# Подготовка временного ряда
ts = daily_sales.set_index("ISSUE_DATE")["REVENUE_AMOUNT"].copy()
ts = ts.asfreq("D").fillna(method="ffill")

# Если в данных есть отрицательные или нулевые значения — добавим маленький сдвиг для лог-преобразований
min_val = ts.min()
shift = 0.0
if min_val <= 0:
    shift = abs(min_val) + 1e-6
    print(f"Найдено min={min_val:.3f} -> добавляю сдвиг {shift:.6f} для лог-преобразования")

forecast_steps = 90

try:
    # Пробуем мультипликативную сезонность (обычно лучше, если амплитуда растёт с уровнем)
    model_hw = ExponentialSmoothing(
        ts,
        trend="add",
        seasonal="mul",
        seasonal_periods=7,
    ).fit()
    use_log = False
    print("Использована модель: trend='add', seasonal='mul'")

except Exception as e:
    # Если мультипликативная модель не сработала — используем лог-преобразование + аддитивную модель
    print("Мультипликативная модель не применима (ошибка), перейду к лог-преобразованию. Ошибка:", e)
    use_log = True

if use_log:
    # лог-преобразование (stabilize variance)
    ts_log = np.log1p(ts + shift)   # log1p для малых значений
    model_hw_log = ExponentialSmoothing(
        ts_log,
        trend="add",
        seasonal="add",
        seasonal_periods=7,
    ).fit()

    forecast_log = model_hw_log.forecast(steps=forecast_steps)
    # обратное преобразование
    forecast_hw = np.expm1(forecast_log) - shift
    # интервал на лог-уровне
    resid = model_hw_log.resid
    resid_std = np.nanstd(resid)
    lower_log = forecast_log - 1.96 * resid_std
    upper_log = forecast_log + 1.96 * resid_std
    lower = np.expm1(lower_log) - shift
    upper = np.expm1(upper_log) - shift

else:
    # Прямая мультипликативная модель
    forecast_hw = model_hw.forecast(forecast_steps)
    resid = model_hw.resid
    resid_std = np.nanstd(resid)
    lower = forecast_hw - 1.96 * resid_std
    upper = forecast_hw + 1.96 * resid_std

# Гарантируем, что прогнозы не отрицательны
forecast_hw = np.maximum(forecast_hw, 0)
lower = np.maximum(lower, 0)
upper = np.maximum(upper, 0)

# ---------------------- Красивый график прогноза ----------------------
plt.figure(figsize=(14, 6))
plt.plot(ts.index, ts.values, label="Фактические продажи", linewidth=2)
plt.plot(forecast_hw.index, forecast_hw.values, "--", label="Прогноз (Holt-Winters)", linewidth=2)

plt.fill_between(
    forecast_hw.index,
    lower,
    upper,
    alpha=0.3,
    label="Доверительный интервал (примерно ±1.96σ)"
)

plt.title("Holt-Winters — прогноз продаж на 90 дней (устойчивый, без отрицаний)")
plt.xlabel("Дата")
plt.ylabel("Сумма продаж")
plt.legend()
plt.tight_layout()
plt.show()

# Дополнительно выведем пару чисел для проверки
print(f"Прогноз (первые 5 значений):\n{forecast_hw.head()}")
print(f"Min прогноза = {forecast_hw.min():.2f}, max прогноза = {forecast_hw.max():.2f}")

print("\nАнализ успешно завершён.")
