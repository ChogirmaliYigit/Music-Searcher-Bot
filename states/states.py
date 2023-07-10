from aiogram.dispatcher.filters.state import StatesGroup, State



class AdminStates(StatesGroup):
    get_music = State()


class UserState(StatesGroup):
    get_category = State()
    search_music_by_cat = State()
    send_music = State()
