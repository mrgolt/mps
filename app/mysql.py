import pymysql

global con
con = pymysql.connect('localhost', 'root', 'ZAQ!@WSX', 'wb')


def add_item(name, artikul, url):
    with con:
        cur = con.cursor()
        query = "INSERT INTO `items` (`name`, `artikul`, `url`) VALUES ('{}', '{}', '{}')".format(name, artikul, url)
        cur.execute(query)


def main():
    with con:
        cur = con.cursor()
        cur.execute("SELECT VERSION()")
        version = cur.fetchone()
        print("Database version: {}".format(version[0]))


if __name__ == '__main__':
    main()