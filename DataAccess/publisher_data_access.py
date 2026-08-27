import sqlite3
from Entities.publisher import Publisher

def get_publisher_list():
    publisher_list = []
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, title
        FROM Publisher
        ORDER BY title
        """)
        rows = cursor.fetchall()
        for row in rows:
            publisher = Publisher(row[0], row[1])
            publisher_list.append(publisher)
    return publisher_list

def insert_publisher(title):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Publisher (title) VALUES (?)", (title,))
        connection.commit()
        return cursor.lastrowid

def update_publisher(publisher_id, title):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Publisher SET title = ? WHERE id = ?
        """, (title, publisher_id))
        connection.commit()
        return True

def delete_publisher(publisher_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Publisher WHERE id = ?", (publisher_id,))
        connection.commit()
        return True

def get_publisher_by_id(publisher_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title FROM Publisher WHERE id = ?", (publisher_id,))
        row = cursor.fetchone()
        if row:
            return Publisher(row[0], row[1])
    return None