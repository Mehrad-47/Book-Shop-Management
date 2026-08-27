class Book:
    def __init__(self, id, title, isbn, price, purchase_price, stock,
                 publication_year, edition_number, author, publisher,
                 genre=None, translator=None):
        self.id = id
        self.title = title
        self.isbn = isbn
        self.price = price
        self.purchase_price = purchase_price
        self.stock = stock
        self.publication_year = publication_year
        self.edition_number = edition_number
        self.author = author
        self.publisher = publisher
        self.genre = genre
        self.translator = translator

    @property
    def profit(self):
        if self.purchase_price:
            return self.price - self.purchase_price
        return 0

    @property
    def profit_percentage(self):
        if self.purchase_price and self.purchase_price > 0:
            return round(((self.price - self.purchase_price) / self.purchase_price) * 100, 1)
        return 0