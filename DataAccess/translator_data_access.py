import sqlite3
from Entities.translator import Translator

def get_translator_list():
    translator_list = []
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, first_name, last_name, phone FROM Translator ORDER BY first_name, last_name")
        rows = cursor.fetchall()
        for row in rows:
            translator = Translator(row[0], row[1], row[2], row[3])
            translator_list.append(translator)
    return translator_list

def insert_translator(first_name, last_name, phone=None):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Translator (first_name, last_name, phone)
        VALUES (?, ?, ?)
        """, (first_name, last_name, phone))
        connection.commit()
        return cursor.lastrowid

def update_translator(translator_id, first_name, last_name, phone=None):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Translator 
        SET first_name = ?, last_name = ?, phone = ?
        WHERE id = ?
        """, (first_name, last_name, phone, translator_id))
        connection.commit()
        return True

def delete_translator(translator_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Translator WHERE id = ?", (translator_id,))
        connection.commit()
        return True

def get_translator_by_id(translator_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, first_name, last_name, phone
        FROM Translator
        WHERE id = ?
        """, (translator_id,))
        row = cursor.fetchone()
        if row:
            return Translator(row[0], row[1], row[2], row[3])
    return None