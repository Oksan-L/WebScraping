import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Старт драйвера
driver = webdriver.Chrome()
driver.get("https://jobs.dou.ua/vacancies/")
driver.maximize_window()

# Чекаємо завантаження першого блоку
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "title"))
)

print("🔽 Починаємо прокручування та завантаження вакансій...")

# Повторне натискання кнопки "Більше вакансій"
while True:
    try:
        # Прокрутка до низу сторінки
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

        # Знаходимо кнопку "Більше вакансій", якщо вона є
        more_button = driver.find_element(By.XPATH, "//div[@class='more-btn']/a")

        # Якщо кнопка видима — натискаємо
        if more_button.is_displayed():
            more_button.click()
            print("➕ Натиснуто 'Більше вакансій'")
            time.sleep(1)
        else:
            print("✅ Кнопка зникла — більше вакансій немає.")
            break

    except:
        print("✅ Кнопку 'Більше вакансій' більше не знайдено.")
        break

# Після завантаження — витягуємо всі посилання
print("📦 Збираємо всі посилання на вакансії...")

vacancy_links = []
elements = driver.find_elements(By.CSS_SELECTOR, "div.title > a.vt")

for el in elements:
    href = el.get_attribute("href")
    title = el.text.strip()
    if href and title:
        vacancy_links.append((title, href))

driver.quit()

# Зберігаємо в CSV
with open("dou_links.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "url"])
    for title, href in vacancy_links:
        writer.writerow([title, href])

print(f"✅ Усього зібрано: {len(vacancy_links)} вакансій. Збережено у dou_links.csv")
