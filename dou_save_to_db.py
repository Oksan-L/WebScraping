import sqlite3
import pandas as pd

# Читання CSV-файлу
df = pd.read_csv("dou_parsed.csv")

# Підключення до SQLite-бази
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
for _, row in df.iterrows():
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
        print(f"❌ Помилка при вставці: {e}")

conn.commit()
conn.close()

print("✅ Дані успішно занесено до бази dou.db")
