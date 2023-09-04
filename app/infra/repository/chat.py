from dataclasses import dataclass

from app.core.models import Chat, Message
from app.core.repository.chat import IChatRepository


@dataclass
class InMemoryChatRepository(IChatRepository):
    chat_lists: list[Chat]

    def create_chat(self, username1: str, username2: str) -> Chat | None:
        chat: Chat = Chat(
            chat_id=len(self.chat_lists),
            username1=username1,
            username2=username2,
            message_list=[],
        )
        self.chat_lists.append(chat)
        return chat

    def get_chat(self, username1: str, username2: str) -> Chat | None:
        for chat in self.chat_lists:
            if (chat.username2 == username2 and chat.username1 == username1) or (
                chat.username2 == username1 and chat.username1 == username2
            ):
                return chat
        return None

    def has_chat(self, username1: str, username2: str) -> bool:
        for chat in self.chat_lists:
            if (chat.username2 == username2 and chat.username1 == username1) or (
                chat.username1 == username2 and chat.username2 == username1
            ):
                return True
        return False

    def add_message(self, message: Message) -> bool:
        for chat in self.chat_lists:
            if (
                chat.username2 == message.sender_username
                and chat.username1 == message.recipient_username
            ) or (
                chat.username2 == message.recipient_username
                and chat.username1 == message.sender_username
            ):
                chat.message_list.append(message)
                return True
        return False

    def get_user_chats(self, username: str) -> list[Chat]:
        user_chats: list[Chat] = []
        for chat in self.chat_lists:
            if chat.username2 == username or chat.username1 == username:
                user_chats.append(chat)
        return user_chats
