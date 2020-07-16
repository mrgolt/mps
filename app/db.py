import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_cat (conn, cat, sql):
    """
    Create a new task
    :param cat:
    :param conn:
    :return:
    """
    cur = conn.cursor()
    try:
        cur.execute(sql, cat)
    except Error as e:
        print(e)

    return cur.lastrowid


def main():
    conn = create_connection(r"pythonsqlite.db")
    sql_categoties = """ CREATE TABLE IF NOT EXISTS categories (
                                            id integer PRIMARY KEY,
                                            lvl1 text NOT NULL,
                                            lvl2 text NOT NULL,
                                            lvl3 text NOT NULL,
                                            url text NOT NULL,
                                            last_update
                                        ); """

    create_table(conn, sql_categoties)
    cat = ('АКСЕССУАРЫ', 'ДЛЯ ЖЕНЩИН', 'СЕРЬГИ', 'http://wb.ru/')
    add_cat(conn, cat)
    conn.commit()

if __name__ == '__main__':
    main()
