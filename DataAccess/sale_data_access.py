import sqlite3
from datetime import datetime

def create_sale(customer_id, items):
    total_amount = sum(
        item["quantity"] * item["unit_price"] - item.get("discount", 0)
        for item in items
    )

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Sale (customer_id, sale_date, total_amount, discount_amount, final_amount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                customer_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_amount,
                0,
                total_amount,
            ),
        )
        sale_id = cursor.lastrowid

        for item in items:
            quantity = item["quantity"]
            unit_price = item["unit_price"]

            cursor.execute(
                """
                INSERT INTO SaleItem (sale_id, book_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
                """,
                (sale_id, item["book_id"], quantity, unit_price),
            )
            cursor.execute(
                "UPDATE Book SET stock = stock - ? WHERE id = ?",
                (quantity, item["book_id"]),
            )

        if customer_id:
            points = int(total_amount / 10)
            if points:
                cursor.execute(
                    "UPDATE Customer SET points = points + ? WHERE id = ?",
                    (points, customer_id),
                )

        connection.commit()
        return sale_id

def get_sale_list():
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT s.id, s.sale_date, c.first_name, c.last_name,
                   s.total_amount, s.final_amount
            FROM Sale s
            LEFT JOIN Customer c ON s.customer_id = c.id
            ORDER BY s.id DESC
            """
        )

        sales = []
        for row in cursor.fetchall():
            sales.append(
                {
                    "id": row[0],
                    "date": row[1],
                    "customer": f"{row[2]} {row[3]}" if row[2] and row[3] else "Unknown Customer",
                    "total": row[4],
                    "paid": row[5],
                    "method": "Cash",
                }
            )
        return sales

def get_sale_items(sale_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT si.id, si.book_id, b.title, si.quantity, si.unit_price
            FROM SaleItem si
            JOIN Book b ON si.book_id = b.id
            WHERE si.sale_id = ?
            """,
            (sale_id,),
        )

        items = []
        for row in cursor.fetchall():
            items.append(
                {
                    "id": row[0],
                    "book_id": row[1],
                    "book_title": row[2],
                    "quantity": row[3],
                    "unit_price": row[4],
                    "discount": 0,
                    "total": row[3] * row[4],
                }
            )
        return items