import db
from parse_foo import get_page_urls
from multiprocessing import Pool
from datetime import datetime
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

    update_queries = []
    insert_queries = []
    try:
        items = get_page_urls(str(row[6]))
        print(len(items))
        for item in items:
            insert_queries.append((item, row[1], row[2], row[3], row[4], row[5]))
        update_queries.append([str(row[0])])
    except:
        print('error ID ' + str(row[0]))


def main():
    conn = db.create_connection(r"cats.db")
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM categories WHERE lvl1 = 'Детям' and last_update IS NULL ORDER BY id DESC ")
    with Pool(5) as p:
        p.map(add_item_urls, rows)
    p.close()
    p.join()
    print(datetime.now() - start_time)


if __name__ == '__main__':
    main()