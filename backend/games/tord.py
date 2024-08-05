import random
import json

from loader import BASE_DIR

class Tord:
    def __init__(self, user_id: str | int, lang_code: str):
        self.user_id = user_id
        self.lang_code = lang_code

        self.truths_list = []
        self.dares_list = []

        self.players_list = []
        self.current_player_number = 0
        self.players_number = 0

        self.players_are_added = False

        self.truth = ""
        self.dare = ""
        self.current_player_name = ""
        self.truth_ist_last_choice = True

        self.reset()
        self.load_gamedata()

    def __str__(self):
        return f"Tord object with id: {self.user_id}"

    def shuffle_lists(self):
        data_lists = [self.truths_list, self.dares_list]
        for the_list in data_lists:
            random.shuffle(the_list)
            random.shuffle(the_list)
            random.shuffle(the_list)

    def out_of_objects(self):
        if len(self.truths_list) == 0 or len(self.dares_list) == 0:
            return True
        else:
            return False

    def reload_gamedata_if_out_of_data(self):
        if len(self.truths_list) == 0 or len(self.dares_list) == 0:
            self.load_gamedata()

    def load_gamedata(self):
        def file(filename):
            target_file = BASE_DIR / 'data' / 'gamedata' / filename
            with open(target_file, mode="r", encoding="utf8") as f:
                return json.load(f)

        for k, v in file("gTruth.json").items():
            self.truths_list.append(v)
        for k, v in file("gDare.json").items():
            self.dares_list.append(v)

        self.shuffle_lists()

    def add_players_names(self, data: str):
        raw_names_list = data.split(sep=",")
        # names_list = []
        for raw_name in raw_names_list:
            name = raw_name.replace(" ", "")
            if name.islower():
                name = name.capitalize()
            self.players_list.append(name)
        # self.players_list = names_list
        self.players_number = len(self.players_list)
        self.current_player_name = self.players_list[self.current_player_number]

    def get_str_of_players_list(self):
        string_names: str = ""
        for name in self.players_list:
            string_names += name
            string_names += ", "
        size = len(string_names)
        string_names = string_names[:size - 2]
        string_names += "."

        return string_names

    def next_player_number(self):
        """
        The function updates the variable 'self.current_player_number' increasing it by 1.
        """
        self.current_player_number += 1
        if self.current_player_number == len(self.players_list):
            self.current_player_number = 0

    def next_player(self):
        self.next_player_number()
        self.current_player_name = self.players_list[self.current_player_number]

    def reset(self):
        self.truths_list = []
        self.dares_list = []

        self.players_list = []
        self.current_player_number = 0
        self.players_number = 0

        self.players_are_added = False

        self.truth = ""
        self.dare = ""
        self.current_player_name = ""