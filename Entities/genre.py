class Genre:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_information(self):
        return f"{self.id}-{self.name}"