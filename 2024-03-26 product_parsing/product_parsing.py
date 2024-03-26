'''Необходимо собрать информацию о представленных HDD на сайте
            и результаты записать в CSV - файл'''


import requests
from bs4 import BeautifulSoup
import csv

csv_header = ['Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объем буферной памяти', 'Цена']

with open('parsing_result.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(csv_header)

for i in range(1, 5):
    url = f'https://parsinger.ru/html/index4_page_{i}.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    for item in soup.find_all('div', class_='item'):
        row = [
            item.find(class_='name_item').text.strip(),
            ' '.join(item.find(lambda tag: tag.name == 'li' and 'Бренд' in tag.text).text.split()[1:]),
            ' '.join(item.find(lambda tag: tag.name == 'li' and 'Форм-фактор' in tag.text).text.split()[1:]),
            ' '.join(item.find(lambda tag: tag.name == 'li' and 'Ёмкость' in tag.text).text.split()[1:]),
            ' '.join(item.find(lambda tag: tag.name == 'li' and 'Объем буферной памяти' in tag.text).text.split()[3:]),
            item.find(class_='price').text
        ]

        with open('parsing_result.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(row)
