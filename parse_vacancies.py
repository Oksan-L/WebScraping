import csv
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Читання посилань з CSV
links = pd.read_csv("workua_links.csv")["vacancy_url"].tolist()

# Старт драйвера
driver = webdriver.Chrome()
driver.maximize_window()

vacancy_data = []

for url in links:
    try:
        # Перехід на сторінку вакансії
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "h1-name"))
        )

        # Назва вакансії
        title = driver.find_element(By.ID, "h1-name").text.strip()

        # Зарплата
        try:
            salary = driver.find_element(
                By.XPATH, "//span[contains(@class, 'glyphicon-hryvnia-fill')]/following-sibling::span"
            ).text.strip()
        except:
            salary = ""

        # Назва компанії
        try:
            company = driver.find_element(
                By.XPATH, "//span[contains(@class, 'glyphicon-company')]/following-sibling::a/span"
            ).text.strip()
        except:
            company = ""

        # Навички
        try:
            skills_elements = driver.find_elements(
                By.XPATH, "//ul[contains(@class, 'js-toggle-block')]//span[@class='ellipsis']"
            )
            skills = [el.text.strip() for el in skills_elements if el.text.strip()]
            skills_str = ", ".join(skills)
        except:
            skills_str = ""

        # Повний опис вакансії
        try:
            description_elem = driver.find_element(By.ID, "job-description")
            description = description_elem.text.strip()
        except:
            description = ""

        # Додаємо до масиву
        vacancy_data.append({
            "title": title,
            "company": company,
            "salary": salary,
            "skills": skills_str,
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
fieldnames = ["title", "company", "salary", "skills", "description", "url"]

with open("workua_parsed.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in vacancy_data:
        writer.writerow({key: row.get(key, "") for key in fieldnames})

print(f"\n✅ Успішно збережено {len(vacancy_data)} вакансій у workua_parsed.csv")
