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
        await message.reply("Xush kelibsiz!", reply_markup=register_user_keyboard())
    else:
        await message.reply("Siz allaqachon ro'yxatdan o'tgansiz.", reply_markup=ReplyKeyboardRemove())
