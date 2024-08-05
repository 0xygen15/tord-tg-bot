from aiogram import types

tof_choice_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [types.KeyboardButton(text="Новый Раунд")],
    [types.KeyboardButton(text="Закончить игру")]
])