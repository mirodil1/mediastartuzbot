import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.reply import register_user_keyboard
from infrastructure.database.repo.requests import RequestsRepo

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo):
    await state.clear()
    submission = await repo.submissions.get_submission_by_tguser_id(message.from_user.id)
    if not submission:
        await message.reply(
            "“Media Start” loyihasining nizomi bilan tanishib chiqing!\n\n"
            "Loyiha nizomi: https://telegra.ph/Media-start-loji%D2%B3asi-NIZOMI-09-09",
            reply_markup=register_user_keyboard(),
        )
    else:
        await message.reply("Siz allaqachon ro'yxatdan o'tgansiz.", reply_markup=ReplyKeyboardRemove())
