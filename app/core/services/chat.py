from dataclasses import dataclass

from app.core.constants import Status
from app.core.models import Chat, Message
from app.core.repository.chat import IChatRepository
from app.core.repository.user import IUserRepository


@dataclass
class ChatService:
    user_repository: IUserRepository
    chat_repository: IChatRepository

    def create_chat(self, username1: str, username2: str) -> tuple[Status, Chat | None]:
        if self.user_repository.has_user(
            username=username1
        ) and self.user_repository.has_user(username=username2):
            chat: Chat = self.chat_repository.create_chat(
                username1=username1, username2=username2
            )
            if chat is None:
                return Status.USER_NOT_FOUND, None
            return Status.OK, chat

    def get_chat(self, username1: str, username2: str) -> tuple[Status, Chat | None]:
        if self.user_repository.has_user(
            username=username1
        ) and self.user_repository.has_user(username=username2):
            chat: Chat = self.chat_repository.get_chat(
                username1=username1, username2=username2
            )
            if chat is None:
                return Status.USER_NOT_FOUND, None
            return Status.OK, chat
        return Status.USER_NOT_FOUND, None

    def send_message(self, message: Message) -> Status:
        if (
            self.user_repository.has_user(username=message.sender_username)
            and self.user_repository.has_user(username=message.recipient_username)
            and self.chat_repository.has_chat(
                username1=message.sender_username, username2=message.recipient_username
            )
        ):
            if not self.chat_repository.add_message(message=message):
                return Status.USER_NOT_FOUND
            return Status.OK

    def get_user_chats(self, username: str) -> tuple[Status, list[Chat]]:
        user_chats: list[Chat] = self.chat_repository.get_user_chats(username=username)
        return Status.OK, user_chats

