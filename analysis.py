# from langdetect import detect
# import sqlite3
#
# conn = sqlite3.connect("dou.db")
# cursor = conn.cursor()
#
# # Витяг всіх описів
# cursor.execute("SELECT id, description FROM vacancies")
# rows = cursor.fetchall()
#
# # Додаємо колонку language, якщо ще нема
# cursor.execute("ALTER TABLE vacancies ADD COLUMN language TEXT")
#
# # Визначаємо мову для кожного опису
# for vacancy_id, description in rows:
#     try:
#         lang = detect(description)
#     except:
#         lang = "unknown"
#
#     cursor.execute("UPDATE vacancies SET language = ? WHERE id = ?", (lang, vacancy_id))
#
# conn.commit()
# conn.close()
#
# print("✅ Мови визначено та збережено в базу.")

import sqlite3
from langdetect import detect, LangDetectException

def detect_language_of_descriptions(db_path: str, table: str):
    # Підключення до бази
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print(f"🔍 Працюємо з базою: {db_path}")

    # Перевіряємо чи існує колонка language — додаємо, якщо ні
    try:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN language TEXT")
        print("➕ Додано колонку 'language'")
    except sqlite3.OperationalError:
        print("ℹ️ Колонка 'language' вже існує — оновлюємо дані")

    # Витягуємо записи, де ще не визначено мову
    cursor.execute(f"SELECT id, description FROM {table} WHERE language IS NULL OR language = ''")
    rows = cursor.fetchall()

    for vacancy_id, description in rows:
        try:
            lang = detect(description)
        except (LangDetectException, TypeError):
            lang = "unknown"

        cursor.execute(f"UPDATE {table} SET language = ? WHERE id = ?", (lang, vacancy_id))

    conn.commit()
    conn.close()
    print(f"✅ Мову визначено для {len(rows)} записів у таблиці '{table}'.")

# Запуск для обох баз:
detect_language_of_descriptions("dou.db", "vacancies")
detect_language_of_descriptions("workua.db", "vacancies")
