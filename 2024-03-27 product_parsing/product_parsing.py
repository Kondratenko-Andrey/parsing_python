'''Необходимо собрать информацию о представленных часах на сайте
            и результаты записать в CSV - файл'''


import requests
from bs4 import BeautifulSoup
import csv


def get_soup(url):
    response_ = requests.get(url)
    response_.encoding = 'utf-8'
    soup_ = BeautifulSoup(response_.text, 'lxml')
    return soup_


csv_headers = ['Наименование', 'Артикул', 'Бренд', 'Модель', 'Тип', 'Технология экрана', 'Материал корпуса',
               'Материал браслета', 'Размер', 'Сайт производителя', 'Наличие', 'Цена', 'Старая цена',
               'Ссылка на карточку с товаром']

with open('parsing_result.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(csv_headers)

for i in range(1, 5):
    soup = get_soup(f'https://parsinger.ru/html/index1_page_{i}.html')

    for watch in soup.find_all('div', class_='item'):
        watch_card_link = 'https://parsinger.ru/html/' + watch.find('a').get('href')
        watch_card_soup = get_soup(watch_card_link).find('div', class_='description')

        table_row = [
            watch_card_soup.find('p', id='p_header').text,
            watch_card_soup.find('p', class_='article').text.split(':')[-1].strip(),
            *[el.split(': ')[1]
              for el in watch_card_soup.find('ul', id='description').text.strip().split('\n')],
            watch_card_soup.find('span', id='in_stock').text.split(': ')[1],
            watch_card_soup.find('span', id='price').text,
            watch_card_soup.find('span', id='old_price').text,
            watch_card_link]

        with open('parsing_result.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(table_row)