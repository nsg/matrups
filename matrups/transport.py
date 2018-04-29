import queue

class Transport:

    def __init__(self):
        self.to_matrix = queue.Queue()
        self.to_hangouts = queue.Queue()

    def send_hangouts(self, obj):
        self.to_hangouts.put(obj)

    def send_matrix(self, obj):
        self.to_matrix.put(obj)
