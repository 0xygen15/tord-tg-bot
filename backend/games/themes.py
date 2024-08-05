import json


class Themes:
    themes_dict: dict = {
        "school": "Школа",
        "work": "Работа",
        "travel": "Путешествия",
        "worldview": "Мировоззрение",
        "social media": "Социальные сети",
        "art": "Искусство",
        "relations": "Отношения",
        "memes": "Мэмы",
        "religion": "Религия",
        "memories": "Воспоминания",
        "if": "Если...",
        "videogames": "Видеоигры",
        "education": "Образование",
        "fashion": "Мода и стиль",
        "hard choice": "Сложный выбор"
    }

    def __str__(self):
        return f"Themes object with id: {self.user_id}"

    @classmethod
    def get_questions(cls, theme_chosen) -> str:
        with open(f"data/gamedata/gThemes.json", mode="r", encoding="utf8") as f:
            file = json.load(f)
            key = cls.get_key(theme_chosen)
            theme_questions_dict = file[key]
        theme_questions_list = [v for k, v in theme_questions_dict.items()]

        theme_questions_string: str = ""
        index = 1
        for item in theme_questions_list:
            spoilered_question = str(index) + ". " + item + "\n" + "***" + "\n"
            theme_questions_string += spoilered_question
            index += 1
        return theme_questions_string

    @classmethod
    def get_themes_names(cls):
        themes_list: list = []
        for key, value in cls.themes_dict.items():
            themes_list.append(value)
        return themes_list

    @classmethod
    def get_key(cls, value):
        key = None
        for k, v in cls.themes_dict.items():
            if v == value:
                key = k
                break
        return key