from aiogram import types
from backend.games.themes import Themes
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def prepare_choice_keyboard():
    # themes_buttons = [types.KeyboardButton(text=str(i)) for i in Themes.get_themes_names()]
    builder = ReplyKeyboardBuilder()
    for button in Themes.get_themes_names():
        builder.add(types.KeyboardButton(text=str(button)))
    builder.add(types.KeyboardButton(text="Закончить игру"))
    builder.adjust(2)

    return builder.as_markup(one_time_keyboard=True, resize_keyboard=True)


themes_choice_keyboard = prepare_choice_keyboard()

themes_new_game_kb = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Закончить игру")]
])





