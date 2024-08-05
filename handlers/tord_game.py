import logging

from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from backend.database import Database
from backend.texts import Texts
from backend.states import TordStates
from backend.keyboards.tord_kbs import tord_choice_keyboard, tord_choice_keyboard2, tord_choice_keyboard_yes_no
from backend.keyboards.info_kb import main_menu_keyboard

from loader import bot

logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(F.text == "Правда или Действие")
async def greeting_and_name_request(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    tord_game_obj = user_obj.tord_game
    tord_game_obj.reset()
    await state.set_state(TordStates.ready_to_get_players_names)

    await bot.send_message(chat_id=message.from_user.id,
                           text=Texts.tord["players names enter request"])


@router.message(TordStates.ready_to_get_players_names)
async def processing_names(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    tord_game_obj = user_obj.tord_game

    tord_game_obj.add_players_names(message.text)
    answer = f"""{Texts.tord["check names"]}\n\n{tord_game_obj.get_str_of_players_list()}\n{Texts.tord["right?"]}"""

    Database.update_user_obj(message.from_user.id, user_obj)

    await state.set_state(TordStates.check_players_names)
    await bot.send_message(chat_id=message.from_user.id, text=answer, reply_markup=tord_choice_keyboard_yes_no)


@router.message(TordStates.check_players_names)
async def proceed_or_retype_names(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    tord_game_obj = user_obj.tord_game

    if message.text == "Да":
        await state.set_state(TordStates.game_request)

        tord_game_obj.load_gamedata()
        answer = tord_game_obj.current_player_name + ", " + Texts.tord["tord?"]
        Database.update_user_obj(message.from_user.id, user_obj)
        await bot.send_message(chat_id=message.from_user.id,
                               text=answer,
                               reply_markup=tord_choice_keyboard)
    elif message.text == "Нет":
        await state.set_state(TordStates.ready_to_get_players_names)
        await bot.send_message(chat_id=message.from_user.id,
                               text=Texts.tord["players names enter request"])


@router.message(TordStates.game_request)
async def game(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    tord_game_obj = user_obj.tord_game

    if message.text == "Правда":
        tord_game_obj.truth = tord_game_obj.truths_list[0]
        tord_game_obj.truth_ist_last_choice = True
        await state.set_state(TordStates.complition_check)
        Database.update_user_obj(message.from_user.id, user_obj)
        await bot.send_message(chat_id=message.from_user.id,
                               text=tord_game_obj.truth,
                               reply_markup=tord_choice_keyboard2)
    elif message.text == "Действие":
        tord_game_obj.dare = tord_game_obj.dares_list[0]
        tord_game_obj.truth_ist_last_choice = False
        await state.set_state(TordStates.complition_check)
        Database.update_user_obj(message.from_user.id, user_obj)
        await bot.send_message(chat_id=message.from_user.id,
                               text=tord_game_obj.dare,
                               reply_markup=tord_choice_keyboard2)
    elif message.text == "Закончить игру":
        await state.clear()
        tord_game_obj.reset()
        Database.update_user_obj(message.from_user.id, user_obj)
        await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)


@router.message(TordStates.complition_check)
async def check(message: Message, state: FSMContext):
    user_obj = Database.get_user_obj_from_db(message.from_user.id)
    tord_game_obj = user_obj.tord_game

    if message.text == "Выполнено":
        if tord_game_obj.truth_ist_last_choice:
            tord_game_obj.truths_list.remove(tord_game_obj.truth)
            tord_game_obj.shuffle_lists()
            tord_game_obj.next_player()
            tord_game_obj.reload_gamedata_if_out_of_data()
            tord_game_obj.truth = tord_game_obj.truths_list[0]
            answer = tord_game_obj.current_player_name + ", " + Texts.tord["tord?"]
            Database.update_user_obj(message.from_user.id, user_obj)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=answer,
                                   reply_markup=tord_choice_keyboard)
            await state.set_state(TordStates.game_request)
        elif not tord_game_obj.truth_ist_last_choice:
            tord_game_obj.dares_list.remove(tord_game_obj.dare)
            tord_game_obj.shuffle_lists()
            tord_game_obj.next_player()
            tord_game_obj.dare = tord_game_obj.dares_list[0]
            Database.update_user_obj(message.from_user.id, user_obj)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=tord_game_obj.dare,
                                   reply_markup=tord_choice_keyboard)
            await state.set_state(TordStates.game_request)

    elif message.text == "Не выполнено":
        if tord_game_obj.truth_ist_last_choice:
            tord_game_obj.shuffle_lists()
            tord_game_obj.truth = tord_game_obj.truths_list[0]
            Database.update_user_obj(message.from_user.id, user_obj)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=tord_game_obj.truth,
                                   reply_markup=tord_choice_keyboard2)
        elif not tord_game_obj.truth_ist_last_choice:
            tord_game_obj.shuffle_lists()
            tord_game_obj.dare = tord_game_obj.dares_list[0]
            Database.update_user_obj(message.from_user.id, user_obj)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=tord_game_obj.dare,
                                   reply_markup=tord_choice_keyboard2)

    elif message.text == "Закончить игру":
        await state.clear()
        tord_game_obj.reset()
        Database.update_user_obj(message.from_user.id, user_obj)
        await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)

