from aiogram.fsm.state import State, StatesGroup

class TordStates(StatesGroup):
    ready_to_get_players_names = State()
    check_players_names = State()
    game_request = State()
    complition_check = State()


class NieStates(StatesGroup):
    game_request = State()
    nie_request = State()
    tord_request = State()
    complition_check = State()

class TofStates(StatesGroup):
    game = State()

class ThemesStates(StatesGroup):
    choice = State()
    game = State()