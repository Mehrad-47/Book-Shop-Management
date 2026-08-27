import sqlite3
from Entities.book import Book
from Entities.author import Author
from Entities.publisher import Publisher
from Entities.genre import Genre
from Entities.translator import Translator

def get_book_list(search_term=None):
    book_list = []

    query = """
    SELECT Book.id,
           Book.title,
           Book.isbn,
           Book.price,
           Book.purchase_price,
           Book.stock,
           Book.publication_year,
           Book.edition_number,
           Book.author_id,
           Author.first_name,
           Author.last_name,
           Book.publisher_id,
           Publisher.title,
           Book.genre_id,
           Genre.name,
           Book.translator_id,
           Translator.first_name,
           Translator.last_name
    FROM Book
    LEFT JOIN Author ON Book.author_id = Author.id
    LEFT JOIN Publisher ON Book.publisher_id = Publisher.id
    LEFT JOIN Genre ON Book.genre_id = Genre.id
    LEFT JOIN Translator ON Book.translator_id = Translator.id
    """

    params = ()
    if search_term:
        value = f"%{search_term}%"
        query += """ WHERE Book.title LIKE ?
                     OR Author.first_name LIKE ?
                     OR Author.last_name LIKE ?
                     OR Publisher.title LIKE ?
                     OR Book.isbn LIKE ?"""
        params = (value, value, value, value, value)

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

        for row in rows:
            author = Author(row[8], row[9], row[10])
            publisher = Publisher(row[11], row[12])

            genre = None
            if row[13] and row[14]:
                genre = Genre(row[13], row[14])

            translator = None
            if row[15] and row[16] and row[17]:
                translator = Translator(row[15], row[16], row[17])

            book = Book(
                row[0], row[1], row[2], row[3], row[4], row[5],
                row[6], row[7], author, publisher, genre, translator
            )
            book_list.append(book)

    return book_list

def insert_book(book_data):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Book (
            title, isbn, price, purchase_price, stock,
            publication_year, edition_number, author_id,
            publisher_id, genre_id, translator_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            book_data['title'],
            book_data['isbn'],
            book_data['price'],
            book_data['purchase_price'],
            book_data['stock'],
            book_data['publication_year'],
            book_data['edition_number'],
            book_data['author_id'],
            book_data['publisher_id'],
            book_data.get('genre_id'),
            book_data.get('translator_id')
        ))
        connection.commit()

def update_book(book_id, book_data):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Book
        SET title = ?,
            isbn = ?,
            price = ?,
            purchase_price = ?,
            stock = ?,
            publication_year = ?,
            edition_number = ?,
            author_id = ?,
            publisher_id = ?,
            genre_id = ?,
            translator_id = ?
        WHERE id = ?
        """, (
            book_data['title'],
            book_data['isbn'],
            book_data['price'],
            book_data['purchase_price'],
            book_data['stock'],
            book_data['publication_year'],
            book_data['edition_number'],
            book_data['author_id'],
            book_data['publisher_id'],
            book_data.get('genre_id'),
            book_data.get('translator_id'),
            book_id
        ))
        connection.commit()

def update_book_stock(book_id, new_stock):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Book SET stock = ? WHERE id = ?
        """, (new_stock, book_id))
        connection.commit()

def get_book_by_id(book_id):
    book_list = get_book_list()
    for book in book_list:
        if book.id == book_id:
            return book
    return None

def delete_book(book_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Book WHERE id = ?", (book_id,))
        connection.commit()