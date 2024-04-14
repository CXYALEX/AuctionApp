class Transaction:
    def __init__(self, id, value, address):
        self.id = id
        self.value = value
        self.address = address

    def encode(self):
        return (str(self.id) + str(self.value) + str(self.address)).encode()
