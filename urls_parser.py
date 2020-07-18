import requests
from bs4 import BeautifulSoup
import csv
from sqldb import add_item
import re


def write_csv(data, name):
    with open(name + '.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)

        writer.writerow((data['id'],
                         data['name'],
                         data['url'],
                         data['brand'],
                         data['sold'],
                         data['price_current'],
                         data['price_prev'],
                         data['rating'],
                         data['reviews'],
                         data['color']))


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    exit(r.status_code)


def write_file_txt(data, name):
    with open(name + '.txt', 'a') as f:
        for line in data:
            f.write(line + '\n')


def get_next_url(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        next_url = 'https://www.wildberries.ru' + soup.find('a', class_='pagination-next').get('href')
    except:
        next_url = None

    return next_url


def get_item_urls(html):
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='dtList i-dtList j-card-item')

    for item in items:
        url = item.find('a', class_='ref_goods_n_p j-open-full-product-card').get('href')

        urls.append(url)
        # print(url)

    # write_file_txt(urls, 'urls')
    return urls


def get_page_urls(url):
    urls = []

    while True:

        html = get_html(url)
        urls += get_item_urls(html)
        url = get_next_url(html)
        if url is None:
            break
    return urls


def main():
    url_list = ['https://www.wildberries.ru/catalog/sport/dlya-detey/detskiy-transport/begovel',
                'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/gigiena-i-uhod?xsubject=999',
                'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/peredvizhenie/perenoski-dlya-detey',
                'https://www.wildberries.ru/catalog/0/search.aspx?search=горка&subject=3594',
                'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/mebel?xsubject=2087',
                'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/mebel/kokony-dlya-novorozhdennyh',
                'https://www.wildberries.ru/catalog/igrushki/konstruktory/magnitnye',
                'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/mebel?xsubject=1982',
                'https://www.wildberries.ru/catalog/detyam/tovary-dlya-malysha/aksessuary-dlya-kormleniya/poilniki']

    for cat_url in url_list:
        #cat_url = 'https://www.wildberries.ru/catalog/sport/dlya-detey/detskiy-transport/begovel'
        urls = get_page_urls(cat_url)
        for url in urls:
            matches = re.search(r"catalog\/(.\d+)", url)
            add_item("",matches[1],url, cat_url)
            print("ADD "+cat_url)


if __name__ == '__main__':
    main()