from aiogram.fsm.state import State, StatesGroup


class AnnouncementSteps(StatesGroup):
    get_announcement_message = State()
    select_button = State()
    get_text_button = State()
    get_url = State()


class CertificateFormSteps(StatesGroup):
    get_full_name = State()


class DialogSteps(StatesGroup):
    start_dialog = State()
