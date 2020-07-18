import pymysql

global con
con = pymysql.connect('localhost', 'root', 'ZAQ!@WSX', 'wb')
con.query("SET time_zone = 'Asia/Yekaterinburg'")


def add_item(name, artikul, url, cat_url):
    with con:
        cur = con.cursor()
        query = "INSERT INTO `items` (`name`, `artikul`, `url`, `cat_url`) VALUES ('{}', '{}', '{}', '{}')".format(name,artikul,url,cat_url)
        cur.execute(query)


def get_last_stocks(artikul):
    with con:
        cur = con.cursor()
        query = "SELECT orders FROM `orders` WHERE `art_id` = {} ORDER BY `timestamp` DESC".format(artikul)
        cur.execute(query)
        try:
            return cur.fetchone()[0]
        except:
            return 0


def main():
    with con:
        cur = con.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        print("Database version: {}".format(version[0]))


if __name__ == '__main__':
    main()