from aiogram.fsm.state import State, StatesGroup


class SubmissionState(StatesGroup):
    full_name = State()
    date_of_birth = State()
    region = State()
    district = State()
    area = State()
    photo = State()
    education = State()
    certificate = State()
    creative_work = State()
    phone_number = State()
