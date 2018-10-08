#! /usr/bin/env python3
import psycopg2

def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.DatabaseError, e:
        print("<Could not connect to database>")


def get_top_articles():
    """Print top 3 articles of all time."""
    db, cursor = connect()
    cursor.execute("""SELECT * FROM (SELECT title, count(*) AS num FROM articles
            JOIN log ON log.path LIKE '%' || articles.slug || '%'
            WHERE status = '200 OK' GROUP by title ORDER by num DESC)
            AS topthree LIMIT 3;""")
    posts = cursor.fetchall()
    db.close()
    for item in posts:
        print("'{}' - {} views".format(item[0], item[1]))


def get_top_authors():
    """Print top authors."""
    db, cursor = connect()
    cursor.execute("""SELECT name, author_views.num FROM authors
            JOIN author_views on authors.id = author_views.author;""")
    posts = cursor.fetchall()
    db.close()
    for item in posts:
        print("{} - {} views".format(item[0], item[1]))


def get_errors():
    """Print days where more than 1% of request lead to errors."""
    db, cursor = connect()
    cursor.execute("""SELECT date, round(cast(percent_errors as numeric), 1)
            as percentage FROM errors_per_day where percent_errors >= 1;""")
    posts = cursor.fetchall()
    db.close()
    for item in posts:
        print("{} - {}% errors ".format(item[0], item[1]))


if __name__ == '__main__':
    print("\nThe most popular three articles of all time are:\n")
    get_top_articles()
    print('\n')
    print("The most popular authors of all time are:\n")
    get_top_authors()
    print('\n')
    print("Days where more that 1% of request lead to errors\n")
    get_errors()
