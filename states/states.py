from aiogram.dispatcher.filters.state import StatesGroup, State



class AdminStates(StatesGroup):
    get_music = State()


class UserState(StatesGroup):
    send_music = State()
