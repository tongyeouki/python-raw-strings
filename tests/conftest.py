class FakeType(type):
    pass


class FakeUser:
    def __init__(self):
        self.first_name = "\bJohn\b"
        self.last_name = "\bDoe\b"
        self.password = "pass\l?word\r"
