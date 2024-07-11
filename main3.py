from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
import matplotlib.pyplot as plt

# Настройка и инициализация драйвера
options = Options()  # Опционально, для работы в фоновом режиме
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, timeout=10)

try:
    # Открытие страницы
    driver.get('https://www.divan.ru/category/divany-i-kresla')
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.i4dRQ')))  # Ожидание загрузки карточек товаров

    # Получение списка карточек товаров
    listings = driver.find_elements(By.CSS_SELECTOR, 'div.lcSMD')

    # Открытие CSV файла для записи
    with open('prices.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Price"])  # Заголовок

        for listing in listings:
            try:
                # Поиск цены внутри карточки
                price = listing.find_element(By.CSS_SELECTOR, 'span.ui-LD-ZU.KIkOH')
                cleaned_price = price.text.replace('₽', '').replace(' ', '').strip()  # Очистка строки от символов валюты и пробелов
                writer.writerow([cleaned_price])
                print(cleaned_price)
            except Exception as e:
                print(f"Ошибка при получении цены: {e}")

finally:
    driver.quit()

def clean_price(price):
    # Удаляем все нецифровые символы и преобразуем в число
    return int(re.sub(r'\D', '', price))

# Чтение данных из исходного CSV файла и их обработка
input_file = 'prices.csv'
output_file = 'cleaned_prices.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, open(output_file, mode='w', newline='',
                                                                  encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Читаем заголовок и записываем его в новый файл
    header = next(reader)
    writer.writerow(header)

    # Обрабатываем и записываем данные строк
    for row in reader:
        try:
            clean_row = [clean_price(row[0])]
            writer.writerow(clean_row)
        except ValueError as e:
            print(f"Ошибка при очистке цены: {e}, строка: {row[0]}")

print(f"Обработанные данные сохранены в файл {output_file}")

# Вычисление средней цены и заполнение списка цен
prices = []
total_price = 0
count = 0

with open(output_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # Пропуск заголовка

    for row in reader:
        try:
            price = int(row[0])
            prices.append(price)  # Добавляем цену в список
            total_price += price
            count += 1
        except ValueError as e:
            print(f"Ошибка при преобразовании цены: {e}")

if count > 0:
    average_price = total_price / count
    print(f"Средняя цена: {average_price:.2f} ₽")
else:
    print("Нет данных для вычисления средней цены")

# Построение гистограммы цен
plt.figure(figsize=(10, 6))
plt.hist(prices, bins=20, edgecolor='black')
plt.title('Гистограмма цен на диваны', fontsize=15)
plt.xlabel('Цена (₽)', fontsize=12)
plt.ylabel('Количество', fontsize=12)
plt.grid(True)
plt.show()