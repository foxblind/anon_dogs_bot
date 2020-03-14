import sqlite3
import config


class DataBase:

    def __init__(self):
        self._base_path = config.BASE_PATH
        self._connection = sqlite3.connect(self._base_path)
        self._connection.row_factory = sqlite3.Row
        self._cursor = self._connection.cursor()

    def add_user(self, user_id: str, first_name: str, last_name: str, user_name: str):
        self._cursor.execute(f"INSERT INTO users "
                             f"values (?, ?, ?, ?, 'new')",
                             (user_id, first_name, last_name or "", user_name or "",))
        self._cursor.execute(f"INSERT INTO chats "
                             f"values(?, '')", (user_id,))
        self._connection.commit()

    def get_user(self, user_id: str):
        return self._cursor.execute(f"SELECT * "
                                    f"from users "
                                    f"WHERE user_id = ?", (user_id,)).fetchone()

    def set_status(self, user_id: str, status: str):
        self._cursor.execute(f"UPDATE users "
                             f"SET status = '{status}' "
                             f"WHERE user_id = '{user_id}'", ())
        self._connection.commit()

    def get_waiting(self):
        return self._cursor.execute(f"SELECT user_id "
                                    f"FROM users "
                                    f"WHERE status = 'waiting'", ()).fetchall()

    def set_companion(self, user_id: str, new_companion_id: str):
        self._cursor.execute(f"UPDATE chats "
                             f"SET companion = ?"
                             f"WHERE user_id = ?", (new_companion_id, user_id))

        self._cursor.execute(f"UPDATE chats "
                             f"SET companion = ? "
                             f"WHERE user_id = ?", (user_id, new_companion_id,))

        r = self._cursor.execute(f"SELECT * "
                                 f"FROM chats_history "
                                 f"WHERE (first_id = {user_id} AND second_id = {new_companion_id}) "
                                 f"OR (first_id = {new_companion_id} AND second_id = {user_id})").fetchone()
        if not r:
            self._cursor.execute(f"INSERT INTO chats_history "
                                 f"values (?, ?, ?)", (user_id, new_companion_id, 1,))
        else:
            self._cursor.execute(f"UPDATE chats_history "
                                 f"SET counter = counter + 1 "
                                 f"WHERE (first_id = {user_id} AND second_id = {new_companion_id}) "
                                 f"OR (first_id = {new_companion_id} AND second_id = {user_id})")
        self._connection.commit()

    def get_companion(self, user_id: str):
        companion = self._cursor.execute(f"SELECT companion "
                                         f"FROM chats "
                                         f"WhERE user_id = ?", (user_id,)).fetchone()[0]
        return str(companion) or ""

    def reset_companion(self, user_id: str):
        companion_id = self._cursor.execute(f"SELECT companion "
                                            f"FROM chats "
                                            f"WhERE user_id = ?", (user_id,)).fetchone()[0]

        self._cursor.execute(f"UPDATE chats "
                             f"SET companion = '' "
                             f"WHERE user_id = ?", (user_id,))

        if len(str(companion_id)):
            self._cursor.execute(f"UPDATE chats "
                                 f"SET companion = '' "
                                 f"WHERE user_id = ?", (companion_id,))
        self._connection.commit()
        return str(companion_id) or ""

    def save_message(self, message_id: str, chat_id: str, sender: str, to: str, text: str, file: str):
        self._cursor.execute(f"INSERT INTO messages "
                             f"values (?, ?, ?, ?, ?, ?)", (message_id, chat_id, sender, to, text, file,))
        self._connection.commit()

    def close(self):
        self._connection.close()

    def save_filtered(self, chat_id: str, message_id: str, from_id: str, to, text: str, file_name: str, file_id: str, content_type: str):
        self._cursor.execute(f"INSERT INTO filtered "
                             f"values (?, ?, ?, ?, ?, ?, ?, ?)",
                             (chat_id, message_id, from_id, to, text, file_name, file_id, content_type,))
        self._connection.commit()

    def get_filtered(self, chat_id: str, message_id: str):
        return self._cursor.execute(f"SELECT file_id, content_type, text "
                                    f"FROM filtered "
                                    f"WHERE chat_id = ?"
                                    f"AND message_id = ?", (chat_id, message_id,)).fetchone()

    def set_admin(self, user_id: str, level: int):
        self._cursor.execute(f"INSERT INTO admins "
                             f"values (?, ?)", (user_id, level))
        self._connection.commit()

    def get_users(self):
        return self._cursor.execute(f"SELECT * "
                                    f"FROM users").fetchall()

    def get_chats_history(self):
        return self._cursor.execute(f"SELECT * "
                                    f"FROM chats_history").fetchall()
        pass

    def get_all_filtered(self):
        return self._cursor.execute(f"SELECT * "
                                    f"FROM filtered").fetchall()
        pass

    def get_messages(self, user):
        user_filter = ""
        if len(user):
            user_filter = f"WHERE from = {user}"

        return self._cursor.execute(f"SELECT * "
                                    f"FROM messages {user_filter}").fetchall()


