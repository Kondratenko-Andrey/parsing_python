import requests
from bs4 import BeautifulSoup
import os

url = 'https://fitseven.ru/myschtsy/atlas-uprajneyniy/bazovyie-uprazhneniya'

# Делаем запрос
response = requests.get(url)
response.encoding = 'utf-8'

# Создаём каталог
if not os.path.exists('test_img_download'):
    # Если папка не существует, создаем её
    os.makedirs('test_img_download')

# Для исключения неоднократных запросов без необходимости, скачиваем html
with open('test_img_download/img.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

# Открываем файл и передаём его в объёкт beautifulsoup
with open('test_img_download/img.html', encoding='utf-8') as file:
    soup = BeautifulSoup(file.read(), 'lxml')

# Получаем необходимые ссылки на изображения
data = map(lambda x: x['src'], soup.find_all('img', attrs={'src': True}))

# Создаём счётчик для наименования картинок
count = 1

# Скачиваем найденные на странице изображения
for row in data:
    response = requests.get(url=row, stream=True)
    with open(f'test_img_download/img{count}.jpg', 'wb') as img:
        img.write(response.content)
        # Увеличиваем счётчик для того, чтобы не было файлов с одинаковым именем
        count += 1
