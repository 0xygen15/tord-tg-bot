from aiogram import types

main_menu_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
    [types.KeyboardButton(text="Правда или Действие"),
     types.KeyboardButton(text="Я никогда не")],
    [types.KeyboardButton(text="Три из пяти"),
     types.KeyboardButton(text="Темы")]
])
