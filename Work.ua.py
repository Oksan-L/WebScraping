import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Користувач вводить кількість сторінок
max_pages = int(input("Скільки сторінок обробити? (введіть число): "))

driver = webdriver.Chrome()
base_url = "https://www.work.ua"
search_url = "https://www.work.ua/jobs-it/?advs=1&page="
# search_url = "https://www.work.ua/jobs-it/?advs=1&days=122&page="

all_links = []

for page in range(1, max_pages + 1):
    url = search_url + str(page)
    driver.get(url)
    print(f"Збираємо сторінку {page}...")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mb-lg"))
        )

        # Знаходимо всі div з вакансіями
        vacancy_blocks = driver.find_elements(By.CLASS_NAME, "mb-lg")

        for block in vacancy_blocks:
            try:
                link = block.find_element(By.TAG_NAME, "a").get_attribute("href")
                if link and "work.ua/jobs/" in link:  # перевірка на правильність посилання
                    all_links.append(link)
            except:
                continue

        print(f"Сторінка {page}: знайдено {len(vacancy_blocks)} вакансій.")

    except Exception as e:
        print(f"Помилка на сторінці {page}:", e)

    time.sleep(1.5)

driver.quit()

# Збереження в CSV
with open("workua_links.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["vacancy_url"])
    for link in all_links:
        writer.writerow([link])

print(f"Усього зібрано {len(all_links)} посилань. Збережено у workua_links.csv")
