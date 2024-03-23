from aiogram.fsm.state import State, StatesGroup


class Steps(StatesGroup):
    get_announcement_message = State()
    select_button = State()
    get_text_button = State()
    get_url = State()
