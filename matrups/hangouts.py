# pylint: disable=missing-docstring

import os

import asyncio
import hangups

from .auth import Auth
from .message import Message

class HangoutsLoginCredentials():
    # pylint: disable=too-few-public-methods

    def __init__(self, email, password, token_file):

        # The bot users email
        self.email = email

        # The bot users password
        self.password = password

        # Path to the file to write the refresh token to
        self.token_file = token_file

class Hangouts():

    def __init__(self, credentials, send_to, transport):
        self.credentials = credentials
        self.send_to = send_to
        self.conversations = None
        self.users = None
        self.info = None
        self.transport = transport
        self.connect()

    def connect(self):
        authenticator = Auth(self.credentials.email, self.credentials.password)
        token_file = os.path.join(os.getcwd(), self.credentials.token_file)
        token = hangups.RefreshTokenCache(token_file)
        auth = hangups.get_auth(authenticator, token)
        self.client = hangups.client.Client(auth)
        self.client.on_connect.add_observer(self.start)
        self.client.on_state_update.add_observer(self.state_update_listener)

    async def runner(self):
        while True:
            await asyncio.sleep(1)
            if not self.transport.to_hangouts.empty():
                message = self.transport.to_hangouts.get()
                await self.send(message.get_message(), message.destination)

    async def get_self_info(self):
        request_header = self.client.get_request_header()
        si_req = hangups.hangouts_pb2.GetSelfInfoRequest(request_header=request_header)
        return await self.client.get_self_info(si_req)

    async def send(self, message, cid):
        # pylint: disable=protected-access
        conversation = self.conversations.get(cid)
        segments = hangups.ChatMessageSegment.from_str(message)
        request = hangups.hangouts_pb2.SendChatMessageRequest(
            request_header=self.client.get_request_header(),
            event_request_header=conversation._get_event_request_header(),
            message_content=hangups.hangouts_pb2.MessageContent(
                segment=[segment.serialize() for segment in segments]
                ),
            annotation=[hangups.hangouts_pb2.EventAnnotation(type=0)]
            )
        await self.client.send_chat_message(request)

    def loop(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(
            self.client.connect(),
            self.runner()
            ))
        loop.close()

    async def state_update_listener(self, state_update):
        if self.is_message_event(state_update):
            event = state_update.event_notification.event
            cid = event.conversation_id.id
            if self.send_to.get(cid):
                uid = event.sender_id.gaia_id
                sender = self.users.get_user(hangups.user.UserID(uid, uid))
                if not sender.is_self:
                    message = Message(
                        self.send_to[cid],
                        sender.full_name,
                        hangups.ChatMessageEvent(event).text
                    )
                    self.transport.send_matrix(message)

    def is_message_event(self, update):
        # pylint: disable=no-self-use
        if update.event_notification:
            event = update.event_notification.event
            if event.event_type == hangups.hangouts_pb2.EVENT_TYPE_REGULAR_CHAT_MESSAGE:
                return True
        return False

    async def start(self):
        self.users, self.conversations = await hangups.build_user_conversation_list(self.client)
        for conv in self.conversations.get_all():
            print("Hangouts: {} ({})".format(conv.id_, conv.name))
