class Customer:
    def __init__(self, id, first_name, last_name, phone, birth_date=None, points=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.birth_date = birth_date
        self.points = points

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def get_information(self):
        return f"{self.id}-{self.first_name} {self.last_name} (Points: {self.points})"