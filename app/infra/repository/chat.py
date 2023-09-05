from dataclasses import dataclass
from sqlite3 import Connection

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


@dataclass
class SqliteChatRepository(IChatRepository):
    connection: Connection

    def _get_chat_messages(self, chat_id: int) -> list[Message]:
        cursor = self.connection.cursor()

        result = []

        for (
            id,
            sender_username,
            recipient_username,
            time,
            text,
            chat_id,
        ) in cursor.execute(
            """
            SELECT * FROM message
             WHERE chat_id = ?
            """,
            [chat_id],
        ):
            message = Message(
                message_id=id,
                sender_username=sender_username,
                recipient_username=recipient_username,
                time=time,
                text=text,
            )

            result.append(message)

        cursor.close()
        return result

    def create_chat(self, username1: str, username2: str) -> Chat | None:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            INSERT INTO chat (username1, username2)
            VALUES (?, ?)
            """,
            [username1, username2],
        )

        if res.lastrowid is None:
            return None

        last_row_id = res.lastrowid

        res = cursor.execute(
            """
            SELECT * FROM chat
             WHERE ROWID = ?
            """,
            [last_row_id],
        )

        chat_id, u1, u2 = res.fetchone()
        chat = Chat(chat_id=chat_id, username1=u1, username2=u2)

        self.connection.commit()
        cursor.close()
        return chat

    def get_chat(self, username1: str, username2: str) -> Chat | None:
        cursor = self.connection.cursor()

        res = cursor.execute(
            """
            SELECT * FROM chat
             WHERE (username1 = ? AND username2 = ?)
                OR (username1 = ? AND username2 = ?)
            """,
            [username1, username2, username2, username1],
        )

        row = res.fetchone()

        if row is None:
            return None

        chat_id, u1, u2 = row
        chat = Chat(
            chat_id=chat_id,
            username1=u1,
            username2=u2,
            message_list=self._get_chat_messages(chat_id=chat_id),
        )

        cursor.close()
        return chat

    def has_chat(self, username1: str, username2: str) -> bool:
        return self.get_chat(username1=username1, username2=username2) is not None

    def add_message(self, message: Message) -> bool:
        cursor = self.connection.cursor()

        chat = self.get_chat(
            username1=message.sender_username, username2=message.recipient_username
        )
        if chat is None:
            return False

        res = cursor.execute(
            """
            INSERT INTO message
            (sender_username, recipient_username, time, text, chat_id)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                message.sender_username,
                message.recipient_username,
                message.time,
                message.text,
                chat.chat_id,
            ],
        )

        if res.rowcount == 0:
            return False

        self.connection.commit()
        cursor.close()
        return True

    def get_user_chats(self, username: str) -> list[Chat]:
        cursor = self.connection.cursor()

        result = []

        for chat_id, username1, username2 in cursor.execute(
            """
            SELECT * FROM chat
             WHERE username1 = ?
                OR username2 = ?
            """,
            [username, username],
        ):
            chat = Chat(
                chat_id=chat_id,
                username1=username1,
                username2=username2,
                message_list=self._get_chat_messages(chat_id=chat_id),
            )

            result.append(chat)

        cursor.close()
        return result
