import logging

from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from backend.database import Database
from backend.texts import Texts
from backend.states import NieStates
from backend.keyboards.tord_kbs import tord_choice_keyboard, tord_choice_keyboard2, tord_choice_keyboard_yes_no
from backend.keyboards.info_kb import main_menu_keyboard
from backend.keyboards.nie_kbs import nie_choice_keyboard

from loader import bot

logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(F.text == "Я никогда не")
async def game_start(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    nie_game_obj = user_obj.nie_game
    nie_game_obj.reset()
    nie_game_obj.load_gamedata()
    Database.update_user_obj(message.from_user.id, user_obj)

    await state.set_state(NieStates.game_request)
    await bot.send_message(chat_id=message.from_user.id,
                           text=nie_game_obj.nie,
                           reply_markup=nie_choice_keyboard)


@router.message(NieStates.game_request)
async def choice_processing(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    nie_game_obj = user_obj.nie_game
    nie_game_obj.reload_gamedata_if_out_of_data()

    if message.text == "Я никогда не ...":
        nie_game_obj.next_nie(remove=True)
        Database.update_user_obj(message.from_user.id, user_obj)
        await bot.send_message(chat_id=message.from_user.id,
                           text=nie_game_obj.nie,
                           reply_markup=nie_choice_keyboard)
    elif message.text == "Правда":
        nie_game_obj.truth_ist_last_choice = True
        Database.update_user_obj(message.from_user.id, user_obj)
        await state.set_state(NieStates.complition_check)
        await bot.send_message(chat_id=message.from_user.id,
                               text=nie_game_obj.truth,
                               reply_markup=tord_choice_keyboard2)
    elif message.text == "Действие":
        nie_game_obj.truth_ist_last_choice = False
        Database.update_user_obj(message.from_user.id, user_obj)
        await state.set_state(NieStates.complition_check)
        await bot.send_message(chat_id=message.from_user.id,
                               text=nie_game_obj.dare,
                               reply_markup=tord_choice_keyboard2)
    elif message.text == "Закончить игру":
        await state.clear()
        nie_game_obj.reset()
        Database.update_user_obj(message.from_user.id, user_obj)

        await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)


@router.message(NieStates.complition_check)
async def completion_check(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    nie_game_obj = user_obj.nie_game
    nie_game_obj.reload_gamedata_if_out_of_data()

    if message.text == "Выполнено":
        if nie_game_obj.truth_ist_last_choice == True:
            nie_game_obj.next_truth(remove=True)
            Database.update_user_obj(message.from_user.id, user_obj)
            await state.set_state(NieStates.game_request)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=nie_game_obj.nie,
                                   reply_markup=nie_choice_keyboard)
        elif nie_game_obj.truth_ist_last_choice == False:
            nie_game_obj.next_dare(remove=True)
            Database.update_user_obj(message.from_user.id, user_obj)
            await state.set_state(NieStates.game_request)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=nie_game_obj.nie,
                                   reply_markup=nie_choice_keyboard)
    elif message.text == "Не выполнено":
        if nie_game_obj.truth_ist_last_choice == True:
            nie_game_obj.next_truth(remove=False)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=nie_game_obj.truth,
                                   reply_markup=tord_choice_keyboard2)
        elif nie_game_obj.truth_ist_last_choice == False:
            nie_game_obj.next_dare(remove=False)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=nie_game_obj.dare,
                                   reply_markup=tord_choice_keyboard2)

    elif message.text == "Закончить игру":
        await state.clear()
        nie_game_obj.reset()
        Database.update_user_obj(message.from_user.id, user_obj)

        await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)
