# pylint: disable=missing-docstring,too-few-public-methods

class Message:

    def __init__(self, destination, sender, message):
        self.destination = destination
        self.sender = sender
        self.message = message

    def get_message(self):
        return "[{}] {}".format(self.sender, self.message)
