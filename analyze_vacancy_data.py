import sqlite3
import pandas as pd
from langdetect import detect, LangDetectException

# Назви таблиць
table_name = "vacancies"

# Завантаження з workua.db
conn_workua = sqlite3.connect("workua.db")
df_workua = pd.read_sql_query(f"SELECT * FROM {table_name}", conn_workua)
conn_workua.close()

# Завантаження з dou.db
conn_dou = sqlite3.connect("dou.db")
df_dou = pd.read_sql_query(f"SELECT * FROM {table_name}", conn_dou)
conn_dou.close()

# 1. Розподіл мов (langdetect результат)
lang_dist_workua = df_workua["language"].value_counts(normalize=True) * 100
lang_dist_dou = df_dou["language"].value_counts(normalize=True) * 100

print("\n📊 Мовна статистика:")
print("Work.ua:\n", lang_dist_workua.round(2))
print("\nDOU:\n", lang_dist_dou.round(2))

# 2. Топ-міста в DOU
top_cities_dou = df_dou["location"].value_counts().head(10)
print("\n🏙️ Топ-10 міст у DOU:\n", top_cities_dou)

# 3. % віддалених вакансій у DOU
remote_percent = df_dou["location"].str.lower().str.contains("віддалено|remote", na=False).mean() * 100
print(f"\n🌍 Віддалені вакансії в DOU: {remote_percent:.2f}%")

# 4. Теги DOU
# tags_series = df_dou['tags'].dropna().str.split(",\s*").explode()
tags_series = df_dou['tags'].dropna().str.split(r",\s*").explode()
top_tags = tags_series.value_counts().head(10)
print("\n🏷️ Топ-10 тегів у DOU:\n", top_tags)

# 5. Навички Work.ua
# skills_series = df_workua['skills'].dropna().str.split(",\s*").explode()
skills_series = df_workua['skills'].dropna().str.split(r",\s*").explode()
top_skills = skills_series.value_counts().head(10)
print("\n🛠️ Топ-10 навичок Work.ua:\n", top_skills)

# 6. Найактивніші компанії
top_companies_workua = df_workua["company"].value_counts().head(10)
top_companies_dou = df_dou["company"].value_counts().head(10)

print("\n🏢 Топ-10 компаній Work.ua:\n", top_companies_workua)
print("\n🏢 Топ-10 компаній DOU:\n", top_companies_dou)
