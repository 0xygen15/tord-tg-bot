import json
import random

from loader import BASE_DIR

class Nie:
    def __init__(self, user_id, lang_code):
        self.user_id = user_id
        self.lang_code = lang_code

        self.truths_list = []
        self.dares_list = []
        self.nevers_list = []

        self.players_list = []

        self.truth = ""
        self.dare = ""
        self.nie = ""

        self.truth_ist_last_choice = True

        self.reset()
        self.load_gamedata()

    def __str__(self):
        return f"Nie object with id: {self.user_id}"

    def shuffle_lists(self):
        data_lists = [self.truths_list, self.dares_list, self.nevers_list]
        for the_list in data_lists:
            random.shuffle(the_list)
            random.shuffle(the_list)
            random.shuffle(the_list)

    def out_of_objects(self):
        if len(self.truths_list) == 0 or len(self.dares_list) == 0 or len(self.nevers_list) == 0:
            return True
        else:
            return False

    def reload_gamedata_if_out_of_data(self):
        if len(self.truths_list) == 0 or len(self.dares_list) == 0 or len(self.nevers_list) == 0:
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
        for k, v in file("gNever.json").items():
            self.nevers_list.append(v)

        self.shuffle_lists()

        self.nie = self.nevers_list[0]
        self.truth = self.truths_list[0]
        self.dare = self.dares_list[0]

    def next_nie(self, remove: bool):
        if remove == True:
            self.nevers_list.remove(self.nie)
        self.shuffle_lists()
        self.nie = self.nevers_list[0]

    def next_truth(self, remove: bool):
        if remove == True:
            self.truths_list.remove(self.truth)
        self.shuffle_lists()
        self.truth = self.truths_list[0]

    def next_dare(self, remove: bool):
        if remove == True:
            self.dares_list.remove(self.dare)
        self.shuffle_lists()
        self.dare = self.dares_list[0]

    def reset(self):
        self.truths_list = []
        self.dares_list = []
        self.nevers_list = []

        self.players_list = []

        self.truth = ""
        self.dare = ""
        self.nie = ""