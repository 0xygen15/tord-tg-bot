import logging

from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext

from backend.games.threeOfFive import ThreeOfFive
from backend.database import Database
from backend.texts import Texts
from backend.states import TofStates
from backend.keyboards.t0f_kbs import tof_choice_keyboard
from backend.keyboards.info_kb import main_menu_keyboard

from loader import bot

logging.basicConfig(level=logging.INFO)

router = Router()


@router.message(F.text == "Три из пяти")
async def three_of_five(message: Message, state: FSMContext):

    truths = ThreeOfFive.three_of_five().get("truths")
    dares = ThreeOfFive.three_of_five().get("dares")

    info = "<i>Ответь на три из пяти вопросов и выполни три из пяти действий</i>" + "\n\n"
    answer = "<b>Вопросы</b>" + "\n" + truths + "\n\n" + "<b>Действия</b>" + "\n" + dares

    await state.set_state(TofStates.game)
    await bot.send_message(chat_id=message.from_user.id,
                           text=info + answer,
                           parse_mode='HTML',
                           reply_markup=tof_choice_keyboard)


@router.message(TofStates.game)
async def game(message: Message, state: FSMContext):

    if message.text == "Новый Раунд":
        truths = ThreeOfFive.three_of_five().get("truths")
        dares = ThreeOfFive.three_of_five().get("dares")

        info = "<i>Ответь на три из пяти вопросов и выполни три из пяти действий</i>" + "\n\n"
        answer = "<b>Вопросы</b>" + "\n" + truths + "\n\n" + "<b>Действия</b>" + "\n" + dares

        await state.set_state(TofStates.game)
        await bot.send_message(chat_id=message.from_user.id,
                               text=info + answer,
                               parse_mode='HTML',
                               reply_markup=tof_choice_keyboard)
    elif message.text == "Закончить игру":
        await state.clear()
        await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)