from typing import Protocol

from app.core.models import Chat, Message


class IChatRepository(Protocol):
    def create_chat(self, username1: str, username2: str) -> Chat:
        pass

    def get_chat(self, username1: str, username2: str) -> Chat:
        pass

    def has_chat(self, username1: str, username2: str) -> bool:
        pass

    def add_message(self, message: Message) -> bool:
        pass
