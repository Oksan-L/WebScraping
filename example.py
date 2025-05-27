from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Налаштування браузера Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Працювати у фоновому режимі без відкриття браузера

# Запуск браузера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Відкриваємо сторінку
url = "https://slovnyk.ua/index.php?swrd=%D0%B2%D0%BA%D1%80%D0%B0%D0%BF%D0%BB%D1%8E%D0%B2%D0%B0%D1%82%D0%B8"
driver.get(url)

# driver.execute_script("window.scrollTo(0, 800)")

# Знаходимо таблицю словоформ
table = driver.find_element(By.CLASS_NAME, "main-table1")

# Отримуємо всі рядки таблиці
rows = table.find_elements(By.TAG_NAME, "tr")

# Зберігаємо дані
data = []
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [cell.text.strip() for cell in cells]
    if row_data:  # Додаємо тільки непорожні рядки
        data.append(row_data)

# Закриваємо браузер
driver.quit()

# Конвертуємо в DataFrame для зручності
df = pd.DataFrame(data)

# Виводимо отриману таблицю в термінал
print(df)

# Зберігаємо дані в CSV
df.to_csv("slovnyk_data.csv", index=False, encoding="utf-8")
print("Дані збережено у файл 'slovnyk_data.csv'")
