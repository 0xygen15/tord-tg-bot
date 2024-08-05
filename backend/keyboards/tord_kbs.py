from aiogram import types

tord_choice_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Правда"),
     types.KeyboardButton(text="Действие")],
    [types.KeyboardButton(text="Закончить игру")]
])

tord_choice_keyboard2 = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Выполнено"),
     types.KeyboardButton(text="Не выполнено")],
    [types.KeyboardButton(text="Закончить игру")]
])

tord_choice_keyboard_yes_no = types.ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
    [types.KeyboardButton(text="Да"),
     types.KeyboardButton(text="Нет")]
])