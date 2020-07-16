from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as BS
from urls_parser import get_html
import db


def get_cats_lvl1(browser):
    url = 'https://www.wildberries.ru'
    browser.get(url)
    bs = BS(browser.page_source, 'lxml')
    # print(browser.page_source)
    tinys = bs.findAll('li', class_='topmenus-item j-parallax-back-layer-item')

    data = []
    for tiny in tinys:
        data.append({'url': tiny.find('a').get('href'), 'text': tiny.find('a').text})

    return data


def get_cats_lvl2(urls):
    data = []
    for url in urls:
        # print(url)
        #if not (url['text'] == 'Цифровые товары' or url['text'] == 'Тренды'):
        if (url['text'] == 'Подарки'):
            bs = BS(get_html(url['url']), 'lxml')
            print(url['url'])
            if url['text'] == 'Спорт':
                lvl2_urls = bs.find('ul', class_='maincatalog-list-1').findAll('a')
            else:
                try:
                    lvl2_urls = bs.find('ul', class_='maincatalog-list-2').findAll('a')
                except:
                    print('ERROR '+url['text'])
                    continue
            for lvl2_url in lvl2_urls:
                if lvl2_url.get('href').find('http') != -1:
                    lvl2 = lvl2_url.get('href')
                else:
                    lvl2 = 'https://wildberries.ru' + lvl2_url.get('href')

                data.append({'lvl1_url': url['url'],
                             'lvl1_name': url['text'],
                             'lvl2_url': lvl2,
                             'lvl2_name': lvl2_url.text,
                             })
    return data


def get_sub_data(url):
    data = []
    bs = BS(get_html(url), 'lxml')
    try:
        hrefs = bs.find('li', class_='selected hasnochild').find('ul').findAll('li')
        for r in hrefs:
            if r.find('http'):
                res = {
                    'url': r.find('a').get('href'),
                    'name': r.find('a').text
                }
                data.append(res)
            else:
                res = {
                    'url': 'https://wildberries.ru' + r.find('a').get('href'),
                    'name': r.find('a').text
                }
                data.append(res)
            # print(res)
        return data
    except:
        return None


def get_sub_cats1(urls):
    conn = db.create_connection(r"cats.db")

    header = {'lvl1_name': '',
              'lvl2_name': '',
              'lvl3_name': '',
              'lvl4_name': '',
              'lvl5_name': '',
              'url': ''}

    for url2 in urls:
        row = header
        row['lvl1_name'] = url2['lvl1_name']
        row['lvl2_name'] = url2['lvl2_name']
        row['url'] = url2['lvl2_url']
        data = get_sub_data(url2['lvl2_url'])
        if not data is None:
            for index, url3 in enumerate(data):
                #if index == 1:
                #   break
                row['lvl3_name'] = url3['name']
                row['url'] = url3['url']
                data = get_sub_data(url3['url'])
                if not data is None:
                    for url4 in data:
                        row['lvl4_name'] = url4['name']
                        row['url'] = url4['url']
                        data = get_sub_data(url4['url'])
                        if not data is None:
                            for url5 in data:
                                row['lvl5_name'] = url5['name']
                                row['url'] = url5['url']
                                print('5 - ')
                                print(row)

                                cat = (row['lvl1_name'], row['lvl2_name'], row['lvl3_name'], row['lvl4_name'],
                                       row['lvl5_name'], row['url'])
                                sql = '''INSERT INTO categories (lvl1,lvl2,lvl3,lvl4,lvl5,url) VALUES(?,?,?,?,?,?)'''
                                db.add_cat(conn, cat, sql)
                                conn.commit()

                                row['lvl5_name'] = ''
                                row['url'] = ''
                        else:
                            print('4 - ')
                            print(row)
                            cat = (
                            row['lvl1_name'], row['lvl2_name'], row['lvl3_name'], row['lvl4_name'], row['lvl5_name'],
                            row['url'])
                            sql = '''INSERT INTO categories (lvl1,lvl2,lvl3,lvl4,lvl5,url) VALUES(?,?,?,?,?,?)'''
                            db.add_cat(conn, cat, sql)
                            conn.commit()
                            row['lvl4_name'] = ''
                            row['url'] = ''
                else:
                    print('3 - ')
                    print(row)
                    cat = (row['lvl1_name'], row['lvl2_name'], row['lvl3_name'], row['lvl4_name'], row['lvl5_name'],
                           row['url'])
                    sql = '''INSERT INTO categories (lvl1,lvl2,lvl3,lvl4,lvl5,url) VALUES(?,?,?,?,?,?)'''
                    db.add_cat(conn, cat, sql)
                    conn.commit()
                    row['lvl3_name'] = ''
                    row['url'] = ''
        else:
            print('2 - ')
            print(row)
            cat = (row['lvl1_name'], row['lvl2_name'], row['lvl3_name'], row['lvl4_name'], row['lvl5_name'], row['url'])
            sql = '''INSERT INTO categories (lvl1,lvl2,lvl3,lvl4,lvl5,url) VALUES(?,?,?,?,?,?)'''
            db.add_cat(conn, cat, sql)
            conn.commit()
            row['lvl1_name'] = ''
            row['lvl2_name'] = ''
            row['url'] = ''


def get_sub_cats(urls):
    data = []
    for url in urls:
        bs = BS(get_html(url['lvl2_url']), 'lxml')
        try:
            hrefs = bs.find('li', class_='selected hasnochild').find('ul').findAll('li')
            for r in hrefs:
                if r.find('http'):
                    res = r.find('a').get('href')
                else:
                    res = 'https://wildberries.ru' + r.find('a').get('href')

                data.append({'lvl1_url': url['lvl1_url'],
                             'lvl1_name': url['lvl1_name'],
                             'lvl2_url': url['lvl2_url'],
                             'lvl2_name': url['lvl2_name'],
                             'lvl3_url': res,
                             'lvl3_name': r.find('a').text})

        except:
            continue
    return data


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    conn = db.create_connection(r"cats.db")

    sql_categoties = """ CREATE TABLE IF NOT EXISTS categories (
                                                id integer PRIMARY KEY,
                                                lvl1 text NOT NULL,
                                                lvl2 text NOT NULL,
                                                lvl3 text NOT NULL,
                                                lvl4 text NOT NULL,
                                                lvl5 text NOT NULL,
                                                url text NOT NULL,
                                                last_update text,
                                                last_data_update text
                                            ); """

    db.create_table(conn, sql_categoties)

    urls = get_cats_lvl1(browser)
    l2 = get_cats_lvl2(urls)
    l3 = get_sub_cats1(l2)
    # l3 = []
    # l3.append({'lvl1_name': 'Зоотовары', 'lvl2_name': 'Для собак', 'lvl3_name': 'Одежда', 'lvl4_name': 'Для мелких и средних пород', 'lvl5_name': 'Попоны', 'url': 'https://wildberries.ru/catalog/aksessuary/tovary-dlya-zhivotnyh/odezhda/dlya-melkih-i-srednih-porod/popony-dlya-zhivotnyh'})

    # for data in l3:
    #    print(data)
    #   cat = (data['lvl1_name'], data['lvl2_name'], data['lvl3_name'], data['lvl4_name'], data['lvl5_name'], data['url'])
    #   sql = '''INSERT INTO categories (lvl1,lvl2,lvl3,lvl4,lvl5,url) VALUES(?,?,?,?,?,?)'''
    #   db.add_cat(conn, cat, sql)
    #   conn.commit()

    browser.quit()


if __name__ == '__main__':
    main()
