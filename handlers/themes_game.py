import logging

from aiogram.types import Message
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
import aiogram.utils.markdown as md

from backend.games.themes import Themes
from backend.database import Database
from backend.texts import Texts
from backend.states import ThemesStates
from backend.keyboards.themes_kbs import themes_choice_keyboard, themes_new_game_kb
from backend.keyboards.info_kb import main_menu_keyboard

from loader import bot

logging.basicConfig(level=logging.INFO)

router = Router()

@router.message(F.text == "Темы")
async def choose_a_theme(message: Message, state: FSMContext):
    await state.set_state(ThemesStates.game)
    await bot.send_message(text="Выбери тему игры:",
                           chat_id=message.from_user.id,
                           reply_markup=themes_choice_keyboard,
                           parse_mode='MarkdownV2')


@router.message(ThemesStates.game)
async def game(message: Message, state: FSMContext):
    answer = message.text
    if answer in Themes.get_themes_names():
        answer_string = Themes.get_questions(theme_chosen=answer)
        info = "Отвечайте каждый на каждый вопрос: \n\n"
        # text = (info + answer_string).replace("-", "\\-")
        await bot.send_message(text=info + answer_string,
                               chat_id=message.from_user.id,
                               parse_mode='HTML',
                               reply_markup=themes_new_game_kb)
    elif answer == "Закончить игру":
        await state.clear()
        await bot.send_message(text=Texts.info["main_menu"], chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)
    else:
        await bot.send_message(text="Нет такой темы!", chat_id=message.from_user.id, parse_mode='HTML',
                               reply_markup=main_menu_keyboard)
