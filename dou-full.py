import pandas as pd
import sqlite3

# === КРОК 1: Об'єднання CSV ===

# Читання окремих частин
df1 = pd.read_csv("dou_parsed-1part.csv")
df2 = pd.read_csv("dou_parsed-2part.csv")
df3 = pd.read_csv("dou_parsed-3part.csv")

# Об'єднання в один DataFrame
merged_df = pd.concat([df1, df2, df3], ignore_index=True)

# Видалення дублікатів за URL
merged_df = merged_df.drop_duplicates(subset="url")

# Збереження у CSV
merged_df.to_csv("dou_merged.csv", index=False, encoding="utf-8")
print(f"✅ Обʼєднано та збережено: {len(merged_df)} вакансій у dou_merged.csv")

# === КРОК 2: Занесення в базу даних ===

# Підключення до SQLite
conn = sqlite3.connect("dou.db")
cursor = conn.cursor()

# Створення таблиці, якщо ще не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    date TEXT,
    location TEXT,
    salary TEXT,
    tags TEXT,
    description TEXT,
    url TEXT UNIQUE
)
""")

# Додавання записів
for _, row in merged_df.iterrows():
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO vacancies (title, company, date, location, salary, tags, description, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("title"),
            row.get("company"),
            row.get("date"),
            row.get("location"),
            row.get("salary"),
            row.get("tags"),
            row.get("description"),
            row.get("url")
        ))
    except Exception as e:
        print(f"❌ Помилка з URL {row.get('url')}: {e}")

conn.commit()
conn.close()
print("✅ Успішно додано в базу dou.db")
