# pylint: disable=missing-docstring

import threading

from matrix_client.client import MatrixClient

from .message import Message

class MatrixLoginCredentials():
    # pylint: disable=too-few-public-methods

    def __init__(self, host, token, userid):

        # The URL to your matrix host/API.
        self.host = host

        # The userid in the form of @user:matrix.server.ltd
        self.userid = userid

        # The above users token
        self.token = token

class Matrix:

    def __init__(self, credentials, rooms, send_to, transport):
        self.credentials = credentials
        self.rooms = rooms
        self.send_to = send_to
        self.transport = transport
        self.connect()

    def connect(self):
        self.client = MatrixClient(self.credentials.host,
                                   token=self.credentials.token,
                                   user_id=self.credentials.userid)

        # Listen for events in all configured rooms
        for room in self.rooms:
            joined_room = self.client.join_room(room)
            joined_room.add_listener(self.listener)

        self.client.start_listener_thread()
        self.print_rooms()
        self.runner()

    def print_rooms(self):
        rooms = self.client.get_rooms()
        for room_id, room in rooms.items():
            print("Matrix: {} ({})".format(room_id, room.display_name))

    def runner(self):
        worker_thread = threading.Timer(1.0, self.runner)
        worker_thread.daemon = True
        worker_thread.start()

        if not self.transport.to_matrix.empty():
            message = self.transport.to_matrix.get()
            self.client.api.send_message(message.destination, message.get_message())

    def listener(self, room, message):
        if self.send_to.get(room.room_id):
            if message.get('content', {}).get('msgtype') == 'm.text':
                if self.credentials.userid != message['sender']:
                    message = Message(
                        self.send_to[room.room_id],
                        message['sender'],
                        message['content']['body']
                    )
                    self.transport.send_hangouts(message)
