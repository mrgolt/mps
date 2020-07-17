from app.mysql import con, get_last_stocks
import requests
from datetime import datetime
import json


def get_artikuls():
    arts = []
    with con:
        cur = con.cursor()
        query = "SELECT artikul FROM `items`"
        cur.execute(query)
        data = cur.fetchall()
        for row in data:
            arts.append(row[0])
    return arts


def add_sales (artikul, orders, sales):
    with con:
        cur = con.cursor()
        query = "INSERT INTO `orders` (art_id, orders, orders_diff,timestamp) VALUES ('{}', '{}', '{}', NOW())".format(artikul, orders, sales)
        cur.execute(query)


def main():
    artikul = ''
    arts = get_artikuls()
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
        print(order_diff, last_orders)
        add_sales(key, arts[key],order_diff)


if __name__ == '__main__':
    main()