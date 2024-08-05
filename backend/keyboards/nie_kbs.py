from aiogram import types

nie_choice_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Я никогда не ...")],
    [types.KeyboardButton(text="Правда"),
     types.KeyboardButton(text="Действие")],
    [types.KeyboardButton(text="Закончить игру")]
])