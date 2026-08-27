import sqlite3
from Entities.customer import Customer

def get_customer_list():
    customer_list = []
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, first_name, last_name, phone, birth_date, points
        FROM Customer
        ORDER BY first_name, last_name
        """)
        rows = cursor.fetchall()
        for row in rows:
            customer = Customer(row[0], row[1], row[2], row[3], row[4], row[5])
            customer_list.append(customer)
    return customer_list

def get_customer_by_phone(phone):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, first_name, last_name, phone, birth_date, points
        FROM Customer
        WHERE phone = ?
        """, (phone,))
        row = cursor.fetchone()
        if row:
            return Customer(row[0], row[1], row[2], row[3], row[4], row[5])
    return None

def insert_customer(first_name, last_name, phone, birth_date=None):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Customer (first_name, last_name, phone, birth_date, points)
        VALUES (?, ?, ?, ?, 0)
        """, (first_name, last_name, phone, birth_date))
        connection.commit()

def update_customer_points(customer_id, points_change):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE Customer
        SET points = points + ?
        WHERE id = ?
        """, (points_change, customer_id))
        connection.commit()