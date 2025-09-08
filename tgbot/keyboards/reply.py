from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def register_user_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="📝 Ro'yxatdan o'tish"),
    )

    return kb.as_markup(resize_keyboard=True)


def skip_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="O'tkazib yuborish"),
    )

    return kb.as_markup(resize_keyboard=True)


def location_keyboard(locations: list[str]) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    for loc in locations:
        kb.row(KeyboardButton(text=loc))

    return kb.as_markup(resize_keyboard=True)
