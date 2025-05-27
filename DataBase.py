import sqlite3
import pandas as pd

# Читання CSV-файлу
df = pd.read_csv("workua_parsed.csv")

# Підключення до SQLite (створиться файл workua.db)
conn = sqlite3.connect("workua.db")
cursor = conn.cursor()

# Створення таблиці, якщо ще не існує
cursor.execute("""
CREATE TABLE IF NOT EXISTS vacancies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    company TEXT,
    salary TEXT,
    skills TEXT,
    description TEXT,
    url TEXT UNIQUE
)
""")

# Додавання записів
for _, row in df.iterrows():
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO vacancies (title, company, salary, skills, description, url)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row.get("title"),
            row.get("company"),
            row.get("salary"),
            row.get("skills"),
            row.get("description"),
            row.get("url")
        ))
    except Exception as e:
        print(f"❌ Помилка при вставці: {e}")

conn.commit()
conn.close()

print(f"✅ Дані успішно додано в базу workua.db")
