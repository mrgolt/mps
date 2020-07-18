from sqldb import con, get_last_stocks
import requests
from datetime import datetime
import json


start_time = datetime.now()


def get_artikuls(limit):
    arts = []
    with con:
        cur_time = datetime.now()
        find_time = datetime(cur_time.year, cur_time.month, cur_time.day, cur_time.hour - 1, cur_time.minute,
                             cur_time.second)
        print(find_time.)
        cur = con.cursor()
        query = "SELECT artikul FROM `items` WHERE `timestamp` < '{}' or `timestamp` IS NULL LIMIT {}".format(find_time,limit)
        cur.execute(query)
        data = cur.fetchall()
        for row in data:
            arts.append(row[0])
    return arts


def add_sales (artikul, orders, sales):
    with con:
        cur = con.cursor()
        if sales is not 0:
            query = "INSERT INTO `orders` (art_id, orders, orders_diff,timestamp) VALUES ('{}', '{}', '{}', '{}')".format(artikul, orders, sales, datetime.now())
            cur.execute(query)
        query = "UPDATE `items` SET `timestamp` = '{}' WHERE `artikul` = '{}'".format(artikul, datetime.now())
        #print(query)
        cur.execute(query)


def main():
    artikul = ''
    arts = get_artikuls(100)
    while len(arts) > 0:
        for art in arts:
            artikul += str(art)+";"

        url_api = 'https://nm-2-card.wildberries.ru/enrichment/v1/api?spp=0&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&nm={}'.format(artikul)
        print(url_api)

        arts = {}
        response = requests.get(url_api)
        if response.status_code == 200:
            js = json.loads(response.text)
            for product in js['data']['products']:
                stocks = 0
                for size in product['sizes']:
                    for wh in size['stocks']:
                        stocks += wh['qty']
                arts[product['id']] = stocks

        for key in arts:
            last_orders = get_last_stocks(key)
            order_diff = last_orders-arts[key] if last_orders > 0 else 0
            add_sales(key, arts[key],order_diff)

        arts = get_artikuls(100)


if __name__ == '__main__':
        main()