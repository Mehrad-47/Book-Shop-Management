import sqlite3
from Entities.author import Author

def get_author_list():
    author_list = []
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, first_name, last_name, phone
        FROM Author
        ORDER BY first_name, last_name
        """)
        rows = cursor.fetchall()
        for row in rows:
            author = Author(row[0], row[1], row[2], row[3])
            author_list.append(author)
    return author_list

def insert_author(first_name, last_name, phone=None):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Author (first_name, last_name, phone)
        VALUES (?, ?, ?)
        """, (first_name, last_name, phone))
        connection.commit()
        return cursor.lastrowid

def update_author(author_id, first_name, last_name, phone=None):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Author 
        SET first_name = ?, last_name = ?, phone = ?
        WHERE id = ?
        """, (first_name, last_name, phone, author_id))
        connection.commit()
        return True

def delete_author(author_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Author WHERE id = ?", (author_id,))
        connection.commit()
        return True

def get_author_by_phone(phone):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, first_name, last_name, phone
        FROM Author
        WHERE phone = ?
        """, (phone,))
        row = cursor.fetchone()
        if row:
            return Author(row[0], row[1], row[2], row[3])
    return None

def get_author_by_id(author_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, first_name, last_name, phone
        FROM Author
        WHERE id = ?
        """, (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(row[0], row[1], row[2], row[3])
    return None