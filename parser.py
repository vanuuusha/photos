import requests
from bs4 import BeautifulSoup
import pandas as pd
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
data = {}


def get_info_about_product(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.content.decode('utf-8'), 'html.parser')
    info = soup.findAll('div', class_="recipeDesc")
    mark = soup.findAll('div', class_="lowFactor noM")
    if len(info) > 0:
        info = info[-1].text
    else:
        info = 'Нет данных'

    if len(mark) > 0:
        mark = mark[0].text[0]
    else:
        mark = 'Нет данных'
    new_dict = {'description': info, 'mark': mark}
    return new_dict


def parse_next_letter(letter, start):
    req = requests.post('http://cosmobase.ru/handbook/search', data={'hbSearch': letter, 'start': start})
    req = req.json()['data']
    soup = BeautifulSoup(req, 'html.parser')
    my_new_divs = soup.findAll('div', class_="searchItem")
    for div in my_new_divs:
        product_name = div.findAll('span', class_="inci_label")[0].text
        link = div.findAll('a', class_="componentLink")[0].get('href')

        if not product_name in data.keys():
            dict_with_extra_data = get_info_about_product(''.join(['http://cosmobase.ru/', link]))
            dict_with_extra_data['link'] = ''.join(['http://cosmobase.ru/', link])
            data[product_name] = dict_with_extra_data

    if len(my_new_divs) != 10:
        return False
    return True


def print_info():
    df = pd.DataFrame({'Name': [product for product in data.keys()],
                       'Link': [data[product]['link'] for product in data],
                       'Description': [data[product]['description'] for product in data],
                       'Save mark': [data[product]['mark'] for product in data]})
    df.to_excel('./teams.xlsx')
    print('Файл Excel создан')


def start_parse():
    for letter in ['q']:
        start = 0
        print(f'Перехожу на букву {letter}')
        while True:
            cont = parse_next_letter(letter, start)
            start += 10
            if not cont:
                break
            print(f'Нахожусь на букве {letter} на {start} компонентах')

    print_info()


if __name__ == '__main__':
    start_parse()
