import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

random.seed(42)
np.random.seed(42)

years = list(range(2021, 2026))  # 2021..2025
n_per_year = {2021: 220, 2022: 240, 2023: 260, 2024: 280, 2025: 300}

first_names = ["Александр","Дмитрий","Максим","Сергей","Илья","Егор","Никита","Михаил","Андрей","Роман",
               "Анна","Мария","Екатерина","Ольга","Ирина","Александра","Елена","Наталья","Светлана","Виктория"]
last_names = ["Иванов","Петров","Сидоров","Кузнецов","Смирнов","Попов","Соколов","Лебедев","Козлов","Новиков",
              "Соколова","Морозова","Васильева","Павлова","Кузьмина","Соловьёва","Егорова","Фёдорова","Медведева","Баранова"]
patronymics_m = ["Иванович","Петрович","Алексеевич","Сергеевич","Михайлович","Никитич","Владимирович","Денисович"]
patronymics_f = ["Ивановна","Петровна","Алексеевна","Сергеевна","Михайловна","Никитична","Владимировна","Денисовна"]

forms = ["очная", "очно-заочная", "заочная"]
specialties = [
    "Информатика и вычислительная техника",
    "Прикладная математика",
    "Физика",
    "Биология",
    "Химия",
    "История",
    "Медицинская биохимия",
    "Экономика"
]

subjects = ["Математика", "Русский язык", "Физика", "Биология", "Химия", "История", "Информатика"]

def gen_phone():
    return "+375" + "".join(str(random.randint(0,9)) for _ in range(9))

def gen_address():
    cities = ["Москва","Санкт-Петербург","Новосибирск","Екатеринбург","Казань","Нижний Новгород","Воронеж","Краснодар","Пермь","Самара"]
    streets = ["Ленина","Советская","Мира","Победы","Центральная","Школьная","Новая","Зелёная","Строителей","Пролетарская"]
    return f"{random.choice(cities)}, ул. {random.choice(streets)}, д. {random.randint(1,200)}, кв. {random.randint(1,200)}"

def gen_fullname(gender):
    if gender == "m":
        first = random.choice(first_names[:10])
        last = random.choice(last_names[:10])
        patron = random.choice(patronymics_m)
    else:
        first = random.choice(first_names[10:])
        last = random.choice(last_names[10:])
        patron = random.choice(patronymics_f)
    return f"{last} {first} {patron}"

records = []

for year in years:
    n = n_per_year.get(year, 200)
    for i in range(n):
        gender = random.choices(["m","f"], weights=[0.52,0.48])[0]
        fio = gen_fullname(gender)
        form = random.choices(forms, weights=[0.65,0.15,0.20])[0]
        taken_subjects = random.sample(subjects, k=3)
        ce_scores = {}
        for subj in subjects:
            if subj in taken_subjects:
                # базовый уровень + небольшая трендовая компонента по годам
                base = 65 + (years.index(year) - 2) * 0.5
                score = np.clip(np.random.normal(loc=base + random.uniform(-5,5), scale=10), 40, 100)
                ce_scores[subj] = round(float(score),1)
            else:
                ce_scores[subj] = np.nan
        cert_avg = np.clip(np.random.normal(loc=78 + (years.index(year)-2)*0.3, scale=6), 50, 100)
        cert_avg = round(float(cert_avg),1)
        specialty = random.choice(specialties)
        ce_taken = [v for v in ce_scores.values() if not pd.isna(v)]
        ce_mean = np.mean(ce_taken) if ce_taken else 60.0
        total_score = round(0.65*ce_mean + 0.35*cert_avg + random.uniform(-2,2),1)
        address = gen_address()
        phone = gen_phone()
        records.append({
            "ФИО": fio,
            "Пол": "М" if gender=="m" else "Ж",
            "Год поступления": year,
            "Форма обучения": form,
            **{f"Балл ЦТ: {s}": ce_scores[s] for s in subjects},
            "Средний балл аттестата": cert_avg,
            "Общий балл при поступлении": total_score,
            "Специальность": specialty,
            "Адрес регистрации": address,
            "Телефон": phone
        })

df = pd.DataFrame(records)

capacities = {}
for year in years:
    for spec in specialties:
        base = 30 if ("Информатика" in spec or "Экономика" in spec) else 20
        cap = int(np.clip(np.random.normal(loc=base, scale=6), 8, 60))
        capacities[(year, spec)] = cap

df["Поступил"] = False
for (year, spec), cap in capacities.items():
    mask = (df["Год поступления"]==year) & (df["Специальность"]==spec)
    sub = df[mask].sort_values("Общий балл при поступлении", ascending=False)
    admitted_idx = sub.head(cap).index
    df.loc[admitted_idx, "Поступил"] = True

cutoffs = []
for year in years:
    for spec in specialties:
        sub = df[(df["Год поступления"]==year) & (df["Специальность"]==spec) & (df["Поступил"])]
        if not sub.empty:
            cutoff = float(sub["Общий балл при поступлении"].min())
            count = len(sub)
        else:
            cutoff = np.nan
            count = 0
        cutoffs.append({"Год": year, "Специальность": spec, "Проходной балл": cutoff, "Поступивших": count})
df_cutoffs = pd.DataFrame(cutoffs)

out_dir = Path.cwd() / "output_data"
out_dir.mkdir(exist_ok=True, parents=True)
csv_path = out_dir / "admissions_synthetic.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
print(f"CSV сохранён: {csv_path}")

subject_means = {}
for subj in subjects:
    yearly = df.groupby("Год поступления")[f"Балл ЦТ: {subj}"].mean()
    subject_means[subj] = yearly

plt.figure(figsize=(10,6))
for subj, series in subject_means.items():
    plt.plot(series.index, series.values, marker='o', label=subj)
plt.title("Динамика среднего балла ЦТ по предметам (среднее по годам)")
plt.xlabel("Год поступления")
plt.ylabel("Средний балл ЦТ (по предмету)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,5))
cert_by_year = df.groupby("Год поступления")["Средний балл аттестата"].mean()
plt.plot(cert_by_year.index, cert_by_year.values, marker='o')
plt.title("Динамика среднего балла аттестата по годам")
plt.xlabel("Год поступления")
plt.ylabel("Средний балл аттестата")
plt.grid(True)
plt.tight_layout()
plt.show()

for spec in specialties:
    spec_df = df_cutoffs[df_cutoffs["Специальность"]==spec].sort_values("Год")
    plt.figure(figsize=(8,4))
    plt.plot(spec_df["Год"], spec_df["Проходной балл"], marker='o')
    plt.title(f"Динамика проходного балла: {spec}")
    plt.xlabel("Год")
    plt.ylabel("Проходной балл (минимум среди поступивших)")
    plt.ylim(40, 100)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

agg_admitted = df[df["Поступил"]].groupby("Специальность")["Поступил"].count().sort_values(ascending=False)
plt.figure(figsize=(10,6))
plt.bar(agg_admitted.index, agg_admitted.values)
plt.title("Количество поступивших студентов по специальностям (всего за 2021-2025)")
plt.xlabel("Специальность")
plt.ylabel("Количество поступивших")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

forms_stats = df[df["Поступил"]].groupby("Форма обучения")["Поступил"].count()
plt.figure(figsize=(6,5))
plt.bar(forms_stats.index, forms_stats.values)
plt.title("Распределение поступивших по формам обучения")
plt.xlabel("Форма обучения")
plt.ylabel("Количество поступивших")
plt.tight_layout()
plt.show()

pivot_cutoff = df_cutoffs.pivot(index="Год", columns="Специальность", values="Проходной балл").round(1)
print("\nПивот-таблица проходных баллов (минимум среди поступивших):")
print(pivot_cutoff)

pivot_path = out_dir / "cutoffs_pivot.csv"
pivot_cutoff.to_csv(pivot_path, encoding="utf-8-sig")
print(f"\nПивот-таблица сохранена: {pivot_path}")

print("\nПример строк данных:")
print(df.head(10).to_string(index=False))
