# Посетить указанный веб-сайт, пройти по всем страницам в категории "мыши" и из каждой карточки товара извлечь артикул.
# После чего все извлеченные артикулы необходимо сложить и представить в виде одного числа.

import requests
from bs4 import BeautifulSoup

# Переменная с итоговым результатом (сумма артикулов)
art_sum = 0
print('Ниже будут указаны все артикулы товаров "Мышь для компьютера": ')
# Необходимо циклично пройти по всем страницам в разделе мыши. В результате анализа обнаружено, что таких страниц - 4
for i in range(1, 5):
    url = f'http://parsinger.ru/html/index3_page_{i}.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')


    # На каждой странице несколько видов искомого продукта с ссылкой на подробную информацию, т.к. видов искомого
    # продукта на странице несколько -> ищем все ссылки для посещения подробной информации
    mouse_links = soup.select('a[href*="mouse/3/"].name_item')
    for el in mouse_links:
        response = requests.get(f'http://parsinger.ru/html/{el["href"]}')
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        art_data = soup.find('p', class_="article").text
        print('\t' + art_data)
        art_sum += int(art_data.split()[-1])

print('-' * 200 + '\n', '-' * 200 + '\n', sep='')
print('Сумма артикулов указанного товара:', art_sum)