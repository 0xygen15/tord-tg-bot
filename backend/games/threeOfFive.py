import random
import json


class ThreeOfFive:

    truths_str = ""
    dares_str = ""

    # def __init__(self, user_id, lang_code):
    #     self.user_id = user_id
    #     self.lang_code = lang_code

    @classmethod
    def three_of_five(cls) -> dict:
        """
        :return: {"truths": truths_str, "dares": dares_str}
        """
        def get_data(filename):

            with open(f"data/gamedata/{filename}.json", mode="r", encoding="utf8") as f:
                the_dict: dict = json.load(f)
                the_list: list = []
                for k, v in the_dict.items():
                    the_list.append(v)

                random.shuffle(the_list)
                random.shuffle(the_list)
                random.shuffle(the_list)

                return the_list[0:5]

        def list_to_string(the_list: list):
            the_string = ""
            for item in the_list:
                the_string += item
                the_string += "\n"
            return the_string

        truths_str = list_to_string(get_data("gTruth"))
        dares_str = list_to_string(get_data("gDare"))

        return {
            "truths": truths_str,
            "dares": dares_str
        }
