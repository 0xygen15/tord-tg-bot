import json


def load_json(filename) -> dict:
    with open(f"./data/texts/{filename}.json", mode="r", encoding="utf8") as f:
        file: dict = json.load(f)
    return file


class Texts:

    info = load_json(filename="info")
    keyboards = load_json(filename="keyboards")
    never = load_json(filename="never_i_ever")
    themes = load_json(filename="themes")
    tord = load_json(filename="truth_or_dare")
    tof = load_json(filename="three_of_five")