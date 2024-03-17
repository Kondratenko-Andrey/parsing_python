# Посетить указанный веб-сайт, систематически пройти по всем категориям, страницам и карточкам товаров (всего 160 шт.).
# Из каждой карточки товара извлечь стоимость и умножить ее на количество товара в наличии.
# Полученные значения агрегировать для вычисления общей стоимости всех товаров на сайте.

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    res_soup = BeautifulSoup(response.text, 'lxml')
    return res_soup


res_sum = 0

for i in range(1, 6):
    soup = get_soup(f'https://parsinger.ru/html/index{i}_page_1.html')

    pagen_links = [el['href']
                   for el in soup.find('div', class_='pagen').find_all('a')]

    for link in pagen_links:
        soup = get_soup(f'https://parsinger.ru/html/{link}')

        product_link = [el.find('a')['href'] for el in soup.find_all('div', class_='sale_button')]

        for prod_el in product_link:
            soup = get_soup(f'https://parsinger.ru/html/{prod_el}')
            res_sum += int(soup.find(id='in_stock').text.split()[-1]) \
                       * int(soup.find(id='price').text.split()[0])

print("Общая стомость всего товара в наличии:", res_sum)
