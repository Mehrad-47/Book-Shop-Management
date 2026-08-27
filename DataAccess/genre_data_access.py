import sqlite3
from Entities.genre import Genre

def get_genre_list():
    genre_list = []
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM Genre ORDER BY name")
        rows = cursor.fetchall()
        for row in rows:
            genre = Genre(row[0], row[1])
            genre_list.append(genre)
    return genre_list

def insert_genre(name):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Genre (name) VALUES (?)", (name,))
        connection.commit()
        return cursor.lastrowid

def update_genre(genre_id, name):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Genre SET name = ? WHERE id = ?
        """, (name, genre_id))
        connection.commit()
        return True

def delete_genre(genre_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Genre WHERE id = ?", (genre_id,))
        connection.commit()
        return True

def get_genre_by_id(genre_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM Genre WHERE id = ?", (genre_id,))
        row = cursor.fetchone()
        if row:
            return Genre(row[0], row[1])
    return None