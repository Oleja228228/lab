import random
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from faker import Faker

RND_SEED = 42
random.seed(RND_SEED)
np.random.seed(RND_SEED)
Faker.seed(RND_SEED)
fake = Faker("ru_RU")

years = list(range(2021, 2026))
n_per_year = {2021: 220, 2022: 240, 2023: 260, 2024: 280, 2025: 300}
subjects = ["Математика", "Русский язык", "Физика", "Биология", "Химия", "История", "Информатика"]

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

def gen_years_list(years, n_per_year):
    lst = []
    for y in years:
        lst.extend([y] * n_per_year[y])
    return lst

def gen_phone_with_faker(n):
    phones = []
    for _ in range(n):
        p = fake.phone_number()
        p = p.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
        phones.append(p)
    return phones

def gen_address_with_faker(n):
    arr = []
    for _ in range(n):
        city = fake.city()
        street = fake.street_name()
        house = fake.building_number()
        apt = fake.random_int(min=1, max=250)
        arr.append(f"{city}, ул. {street}, д. {house}, кв. {apt}")
    return arr

def make_patronymic_from_father(father_name: str, gender: str):
    fn = father_name.strip()
    if not fn:
        return ""
    last_char = fn[-1]
    if last_char in ("а", "я"):
        stem = fn[:-1]
        male = stem + "ович"
        female = stem + "овна"
    elif last_char == "й":
        stem = fn[:-1]
        male = stem + "евич"
        female = stem + "евна"
    elif last_char == "ь":
        stem = fn[:-1]
        male = stem + "евич"
        female = stem + "евна"
    else:
        male = fn + "ович"
        female = fn + "овна"
    return male if gender == "m" else female

def gen_full_names_faker(n, genders_array):
    fio = []
    for g in genders_array:
        if g == "m":
            first = fake.first_name_male()
            last = fake.last_name_male()
        else:
            first = fake.first_name_female()
            last = fake.last_name_female()
        # отец — всегда мужское имя
        father = fake.first_name_male()
        patron = make_patronymic_from_father(father, g)
        fio.append(f"{last} {first} {patron}")
    return fio

years_list = gen_years_list(years, n_per_year)
N = len(years_list)

genders = np.array([fake.random_element(elements=("m", "f")) for _ in range(N)])

forms_arr = [fake.random_element(elements=forms) for _ in range(N)]
specialties_arr = [fake.random_element(elements=specialties) for _ in range(N)]

fio_arr = gen_full_names_faker(N, genders)
phones = gen_phone_with_faker(N)
addresses = gen_address_with_faker(N)

taken_subjects = [fake.random_elements(elements=subjects, length=3, unique=True) for _ in range(N)]

df = pd.DataFrame({
    "ФИО": fio_arr,
    "Пол": np.where(genders == "m", "М", "Ж"),
    "Год поступления": years_list,
    "Форма обучения": forms_arr,
    "Специальность": specialties_arr,
    "Адрес регистрации": addresses,
    "Телефон": phones
})

year_index = df["Год поступления"].map(lambda y: years.index(y))  # 0..4
cert_loc = 78 + (year_index - 2) * 0.3
cert_avgs = np.clip(np.random.normal(loc=cert_loc, scale=6.0), 50, 100).round(1)
df["Средний балл аттестата"] = cert_avgs

for subj in subjects:
    df[f"Балл ЦТ: {subj}"] = np.nan

for i, subj_list in enumerate(taken_subjects):
    y = df.at[i, "Год поступления"]
    base = 65 + (years.index(y) - 2) * 0.5
    for subj in subj_list:
        score = float(np.clip(np.random.normal(loc=base + random.uniform(-5, 5), scale=10.0), 40, 100))
        df.at[i, f"Балл ЦТ: {subj}"] = round(score, 1)

subj_cols = [f"Балл ЦТ: {s}" for s in subjects]
df["CE_mean"] = df[subj_cols].mean(axis=1)
df["Общий балл при поступлении"] = (
    0.65 * df["CE_mean"] + 0.35 * df["Средний балл аттестата"] + np.random.uniform(-2, 2, size=N)
).round(1)

pairs = pd.MultiIndex.from_product([years, specialties], names=["Год", "Специальность"])
base_vals = [30 if ("Информатика" in spec or "Экономика" in spec) else 20 for spec in specialties]
base_repeated = np.tile(base_vals, len(years))
caps = np.clip(np.random.normal(loc=base_repeated, scale=6.0), 8, 60).round().astype(int)
capacities = pd.DataFrame({
    "Год": pairs.get_level_values(0),
    "Специальность": pairs.get_level_values(1),
    "Вместимость": caps
})

df["Поступил"] = False

def admit_top_k(group):
    year = group.name[0]
    spec = group.name[1]
    k = capacities.loc[(capacities["Год"] == year) & (capacities["Специальность"] == spec), "Вместимость"].iat[0]
    if k <= 0:
        return pd.Series(False, index=group.index)
    top_idx = group["Общий балл при поступлении"].nlargest(k).index
    mask = group.index.isin(top_idx)
    return pd.Series(mask, index=group.index)

grouped = df.groupby(["Год поступления", "Специальность"])
admitted_mask = grouped.apply(lambda g: admit_top_k(g), include_groups=False).reset_index(level=[0,1], drop=True)
df.loc[admitted_mask.index, "Поступил"] = admitted_mask.values.astype(bool)

cutoffs = df[df["Поступил"]].groupby(["Год поступления", "Специальность"])["Общий балл при поступлении"].min().reset_index()
cutoffs = cutoffs.rename(columns={"Год поступления": "Год", "Общий балл при поступлении": "Проходной балл"})
pivot_cutoff = cutoffs.pivot(index="Год", columns="Специальность", values="Проходной балл").reindex(index=years)

out_dir = Path.cwd() / "output_data"
out_dir.mkdir(exist_ok=True, parents=True)
csv_path = out_dir / "admissions_synthetic_all_faker.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
pivot_path = out_dir / "cutoffs_pivot_all_faker.csv"
pivot_cutoff.to_csv(pivot_path, encoding="utf-8-sig")

print(f"CSV сохранён: {csv_path}")
print(f"Пивот-таблица сохранена: {pivot_path}")

subject_means = df.groupby("Год поступления")[subj_cols].mean().rename(columns=lambda c: c.replace("Балл ЦТ: ", ""))
plt.figure(figsize=(10, 6))
for col in subject_means.columns:
    plt.plot(subject_means.index, subject_means[col], marker='o', label=col)
plt.title("Динамика среднего балла ЦТ по предметам (среднее по годам)")
plt.xlabel("Год поступления")
plt.ylabel("Средний балл ЦТ (по предмету)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

cert_by_year = df.groupby("Год поступления")["Средний балл аттестата"].mean()
plt.figure(figsize=(8, 5))
plt.plot(cert_by_year.index, cert_by_year.values, marker='o')
plt.title("Динамика среднего балла аттестата по годам")
plt.xlabel("Год поступления")
plt.ylabel("Средний балл аттестата")
plt.grid(True)
plt.tight_layout()
plt.show()

for spec in specialties:
    if spec in pivot_cutoff.columns:
        ser = pivot_cutoff[spec]
        if ser.notna().any():
            plt.figure(figsize=(8, 4))
            plt.plot(ser.index, ser.values, marker='o')
            plt.title(f"Динамика проходного балла: {spec}")
            plt.xlabel("Год")
            plt.ylabel("Проходной балл (минимум среди поступивших)")
            plt.ylim(40, 100)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

agg_admitted = df[df["Поступил"]].groupby("Специальность")["Поступил"].count().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
agg_admitted.plot(kind="bar")
plt.title("Количество поступивших студентов по специальностям (всего за 2021-2025)")
plt.xlabel("Специальность")
plt.ylabel("Количество поступивших")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

forms_stats = df[df["Поступил"]].groupby("Форма обучения")["Поступил"].count()
plt.figure(figsize=(6, 5))
forms_stats.plot(kind="bar")
plt.title("Распределение поступивших по формам обучения")
plt.xlabel("Форма обучения")
plt.ylabel("Количество поступивших")
plt.tight_layout()
plt.show()

print("\nПример строк данных:")
print(df.head(10).to_string(index=False))
print("\nПивот-таблица проходных баллов (минимум среди поступивших):")
print(pivot_cutoff.round(1))
