from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# 🔹 ПОСИЛАННЯ НА ПОШУК ВАКАНСІЙ (без авторизації)
JOBS_URL = "https://www.linkedin.com/jobs/search/?currentJobId=4146731320&geoId=102264497&keywords=%D0%A0%D0%BE%D0%B7%D1%80%D0%BE%D0%B1%D0%BD%D0%B8%D0%BA%20Python&origin=JOB_SEARCH_PAGE_KEYWORD_AUTOCOMPLETE&refresh=true"

# 🔹 Налаштування Selenium
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Запускаємо WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 1️⃣ Переходимо на сторінку пошуку вакансій
driver.get(JOBS_URL)
time.sleep(5)  # Чекаємо завантаження сторінки

# 2️⃣ Шукаємо і натискаємо кнопку `modal__dismiss`
try:
    close_button = driver.find_element(By.XPATH, "//button[contains(@class, 'modal__dismiss')]")
    ActionChains(driver).move_to_element(close_button).click().perform()
    print("Вікно закрито (натиснута кнопка `modal__dismiss`).")
    time.sleep(2)  # Дати сторінці оновитись
except Exception as e:
    print("Не вдалося знайти або натиснути на кнопку `modal__dismiss`:", str(e))

# 3️⃣ Прокручуємо всю сторінку кілька разів перед збором вакансій
for i in range(5):  # 5 разів прокручуємо вниз
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    print(f"Прокручування сторінки {i+1}/5...")
    time.sleep(2)  # Чекаємо підвантаження контенту

# 4️⃣ Збираємо вакансії, компанії та посилання
try:
    job_listings = driver.find_elements(By.XPATH, "//a[contains(@class, 'base-card__full-link')]")

    job_data = []

    for job in job_listings:
        try:
            # Назва вакансії (основний метод)
            job_title = "Не знайдено"
            try:
                job_title_elem = job.find_element(By.XPATH, ".//span[@class='sr-only']")
                job_title = job_title_elem.text.strip() if job_title_elem.text.strip() else "Не знайдено"
            except:
                pass  # Продовжуємо, якщо назва не знайдена

            # Якщо основний метод не працює, пробуємо зчитати весь текст <a>
            if job_title == "Не знайдено":
                job_title = job.text.strip() if job.text.strip() else "Не знайдено"

            # Посилання на вакансію
            job_link = job.get_attribute("href") if job else "Посилання не знайдено"

            job_data.append((job_title, job_link))
        except Exception as e:
            print(f"Проблема з одним записом: {str(e)}")

    # Виводимо всі вакансії та посилання
    print("\n🔹 Знайдені вакансії:")
    for i, (title, link) in enumerate(job_data, 1):
        print(f"{i}. {title} ({link})")

except Exception as e:
    print("Помилка при зборі даних:", str(e))

# Закриваємо браузер
driver.quit()
