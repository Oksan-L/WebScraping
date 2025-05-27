import csv
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Читання посилань з CSV
links_df = pd.read_csv("dou_links.csv")
# links = links_df["url"].tolist()
links = links_df["url"].tolist()[5354:]  # елементи з індексу 2559 (тобто 2560-й і далі)
# links = links_df["url"].tolist()[:20]  # тільки перші 20 посилань

driver = webdriver.Chrome()
driver.maximize_window()

results = []

for url in links:
    try:
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "b-typo"))
        )

        # Назва вакансії
        try:
            title = driver.find_element(By.CLASS_NAME, "g-h2").text.strip()
        except:
            title = ""

        # Назва компанії
        try:
            company = driver.find_element(By.CSS_SELECTOR, "a.company").text.strip()
        except:
            company = ""

        # Дата публікації (обрізання після 202X)
        try:
            date_block = driver.find_element(By.CLASS_NAME, "date")
            full_text = date_block.text.strip()

            match = re.search(r"202[0-9]", full_text)
            if match:
                end_index = match.end()
                date = full_text[:end_index].strip()
            else:
                date = full_text.strip()
        except:
            date = ""

        # Розташування
        try:
            location = driver.find_element(By.CSS_SELECTOR, "div.sh-info > span.place").text.strip()
        except:
            location = ""

        # Зарплата
        try:
            salary = driver.find_element(By.CSS_SELECTOR, "div.sh-info > span.salary").text.strip()
        except:
            salary = ""

        # Теги (badge)
        try:
            tags = ", ".join(
                badge.text.strip()
                for badge in driver.find_elements(By.CSS_SELECTOR, "div.date > a.badge")
                if badge.text.strip()
            )
        except:
            tags = ""

        # Опис вакансії
        try:
            description = driver.find_element(By.CSS_SELECTOR, "div.b-typo.vacancy-section").text.strip()
        except:
            description = ""

        # Збереження результату
        results.append({
            "title": title,
            "company": company,
            "date": date,
            "location": location,
            "salary": salary,
            "tags": tags,
            "description": description,
            "url": url
        })

        print(f"✔️ Оброблено: {title}")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Помилка з {url}: {e}")
        continue

driver.quit()

# Збереження у CSV
fieldnames = ["title", "company", "date", "location", "salary", "tags", "description", "url"]

with open("dou_parsed.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow({key: row.get(key, "") for key in fieldnames})

print(f"\n✅ Успішно збережено {len(results)} вакансій у dou_parsed.csv")
