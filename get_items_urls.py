import db
import re
from parse_foo import get_page_urls
from multiprocessing import Pool
from datetime import datetime
from google.cloud import bigquery

start_time = datetime.now()


def add_multi_urls():
    conn = db.create_connection(r"cat5test.db")
    cursor = conn.cursor()
    update_queries = []
    insert_queries = []
    while True:
        for row in cursor.execute('SELECT * FROM categories WHERE last_update IS NULL ORDER BY id DESC LIMIT 5'):
            try:
                items = get_page_urls(str(row[6]))
                print(len(items))
                for item in items:
                    insert_queries.append((item, row[1], row[2], row[3], row[4], row[5]))
                update_queries.append([str(row[0])])
            except:
                print('error ID ' + str(row[0]))
                continue
                update_queries = []
                insert_queries = []
        cursor.executemany("UPDATE categories SET last_update = date('now') WHERE id = (?)", update_queries)
        cursor.executemany("INSERT INTO items (url,lvl1,lvl2,lvl3,lvl4,lvl5) VALUES (?,?,?,?,?,?)", insert_queries)
        conn.commit()


def add_item_urls(row):
    client = bigquery.Client.from_service_account_json(
        'warm-composite-280714-d0e0c8faac10.json')
    table = client.get_table("wb.items")

    insert_queries = []

    items = get_page_urls(str(row[5]))
    print(len(items))
    for item in items:
        matches = re.search(r"catalog\/(.\d+)", item)
        insert_queries.append(
            {'articul': matches[1], 'url': item, 'lvl1': row[0], 'lvl2': row[1], 'lvl3': row[2], 'lvl4': row[3],
             'lvl5': row[4]})
        if len(insert_queries) >= 100:
            client.insert_rows(table, insert_queries)
            print(insert_queries)
            insert_queries.clear()
    client.insert_rows(table, insert_queries)
    print(insert_queries)


def main():
    client = bigquery.Client.from_service_account_json(
        'warm-composite-280714-d0e0c8faac10.json')

    query_job = client.query("SELECT * FROM wb.category WHERE lvl5 not like '%Сменные файлы для пилок%'")

    rows = []
    for row in query_job:
        rows.append((str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])))

    with Pool(5) as p:
        p.map(add_item_urls, rows)
    p.close()
    p.join()
    print(datetime.now() - start_time)


if __name__ == '__main__':
    main()
