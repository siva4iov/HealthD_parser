import time
import random
import requests
from bs4 import BeautifulSoup
import json
import csv
#
# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36 OPR/78.0.4093.184'
}
# req = requests.get(url, headers=headers)
# src = req.text

# with open('index.html', 'w', encoding="utf=8") as file:
#     file.write(src)

with open('index.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
# all_products_dict = {}
# for item in all_products_hrefs:
#     item_title = item.text
#     item_href = 'https://health-diet.ru' + item['href']
#
#     all_products_dict[item_title] = item_href
#
# with open('all_products_dict.json', 'w', encoding='utf-8') as file:
#     json.dump(all_products_dict, file, indent=4, ensure_ascii=False)
#
with open('all_products_dict.json', encoding='utf-8') as file:
    all_products_dict = json.load(file)
count = 0
length = len(all_products_dict)
for category_name, category_href in all_products_dict.items():
    repl = [' ', '-', ',', "\'"]
    for item in repl:
        if item in category_name:
            category_name = category_name.replace(item, '_')

    req = requests.get(category_href, headers=headers)
    src = req.text
    #
    # with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8') as file:
    #     file.write(src)
    #
    # with open(f'data/{count}_{category_name}.html', encoding='utf-8') as file:
    #     src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    table_row = soup.find('table').find('tr').find_all('th')
    product = table_row[0].text
    ccal = table_row[1].text
    proteins = table_row[2].text
    fats = table_row[3].text
    carbohydrates = table_row[4].text

    with open(f'data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow((
            product,
            ccal,
            proteins,
            fats,
            carbohydrates
        ))
    product_data = soup.find('table').find('tbody').find_all('tr')

    for item in product_data:
        product_tds = item.find_all('td')
        title = product_tds[0].text
        ccal = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                title,
                ccal,
                proteins,
                fats,
                carbohydrates
            ))

    count += 1
    print(f'{title} is downloaded')
    print(f'Progress: {count}/{length} ')
    time.sleep(random.randrange(2, 4))