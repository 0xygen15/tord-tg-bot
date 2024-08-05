import logging

from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext

from loader import bot
from backend.users import Users
from backend.texts import Texts
from backend.games.tord import Tord
from backend.games.nie import Nie
from backend.database import Database
from backend.keyboards.info_kb import main_menu_keyboard

router = Router()


@router.message(Command("info", prefix="/"))
async def info(message: Message):
    await bot.send_message(text=Texts.info["info"], chat_id=message.from_user.id, parse_mode='HTML')


# @dp.message(Command("main_menu"))
@router.message(Command("start", prefix="/"))
async def start(message: Message, state: FSMContext):
    await state.clear()
    try:
        user_obj = Database.get_user_obj_from_db(message.from_user.id)
    except Exception as e:
        logging.error(f'Error {e} occured in start_handler')
        lang_code = message.from_user.language_code

        user = Users(
            user_id=message.from_user.id,
            lang_code=lang_code,
            tord_game=Tord(message.from_user.id, lang_code),
            nie_game=Nie(message.from_user.id, lang_code),
            chat_id=message.chat.id,
            chat_type=message.chat.type,
            username=message.from_user.username,
            fName=message.from_user.first_name,
            lName=message.from_user.last_name,
        )

        # Database.create_users_table() # create db if not created
        Database.add_user_to_db(user) #add user data to db if bot added yet
        logging.info("New user added")

        user_obj = Database.get_user_obj_from_db(message.from_user.id)
        logging.info("User retrieved")

    await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                           reply_markup=main_menu_keyboard)
