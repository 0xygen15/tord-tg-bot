from backend.games.nie import Nie
from backend.games.tord import Tord


class Users:
    def __init__(self, user_id: str | int,
                 lang_code: str,
                 tord_game: Tord,
                 nie_game: Nie,
                 chat_id: str | int,
                 chat_type: str,
                 username: str,
                 fName: str,
                 lName: str):

        self.user_id = user_id
        self.lang_code = lang_code

        self.tord_game = tord_game
        self.nie_game = nie_game

        self.chat_id = chat_id
        self.chat_type = chat_type
        self.username = username
        self.fName = fName
        self.lName = lName


