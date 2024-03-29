import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent


def get_soup(url):
    '''Функция осуществления запроса и возврата Beautiful soup объекта'''

    response_ = session.get(url)
    response_.encoding = 'utf-8'
    soup_ = BeautifulSoup(response_.text, 'lxml')
    return soup_


def get_data_row(data):
    '''Функция принимает выгрузку тега и формирует список со значениями для записи в csv файл'''

    tags = [
        ('p', {'id': 'p_header'}),
        ('p', {'class': 'article'}),
        ('li', {'id': 'brand'}),
        ('li', {'id': 'model'}),
        ('span', {'id': 'in_stock'}),
        ('span', {'id': "price"}),
        ('span', {'id': "old_price"}),
    ]

    row_data = list(map(lambda el: el.split(': ')[1].strip() if ':' in el else el.strip(),
                        [data.find(tag, attrs).text for tag, attrs in tags]))

    return row_data


# Базовый url удобен для составления последующих ссылок
base_url = 'https://parsinger.ru/html/'
user_agent = UserAgent()

session = requests.Session()
session.headers.update({'User-Agent': user_agent.random})

# Создаём csv файл и записываем заголовки
csv_product_headers = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена', 'Старая цена', 'Ссылка']

with open('product.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(csv_product_headers)

# Т.к. количество ссылок небольшое, то оно задано вручную, чтобы не загромождать код
for i in range(1, 6):
    for j in range(1, 5):

        # Получаем разделы тегов на каждый товар
        soup = get_soup(f'{base_url}index{i}_page_{j}.html').find_all('div', class_='item')

        for product in soup:
            # Формируем ссылку на карточку товара
            product_link = f'{base_url}{product.find("a").get("href")}'

            # Используя полученную ссылку получаем содержание тега с описанием товара
            product_card_soup = get_soup(product_link).find('div', class_="description")

            # Получаем список с необходимыми значениями для строки csv файла
            product_row = get_data_row(product_card_soup)
            product_row.append(product_link)

            with open('product.csv', 'a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(product_row)

print('Файл product.csv создан.')
