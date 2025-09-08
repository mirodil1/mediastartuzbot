import os
import re
import logging
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext

from infrastructure.database.repo.requests import RequestsRepo
from infrastructure.database.models import TgUser
from misc.states import SubmissionState
from keyboards.reply import skip_keyboard, location_keyboard


submission_router = Router()


@submission_router.message(F.text == "📝 Ro'yxatdan o'tish")
async def user_start(message: Message, state: FSMContext, repo: RequestsRepo):
    submission = await repo.submissions.get_submission_by_tguser_id(message.from_user.id)
    if submission:
        await message.reply(
            "Siz allaqachon ro'yxatdan o'tgansiz.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    await state.set_state(SubmissionState.full_name)

    await message.answer(
        "<b>Familiya, ism va sharifingizni kiriting.</b>\n"
        "<i>(Abdullayev Abdullajon Abdulla o'g'li)</i>",
        reply_markup=ReplyKeyboardRemove()
    )


@submission_router.message(SubmissionState.full_name, F.text)
async def process_full_name(message: Message, bot: Bot, state: FSMContext):
    full_name = message.text.strip()
    if len(full_name.split()) < 3:
        await message.answer(
            "<b>To'liq ismni to'g'ri kiriting.</b>\n"
            "<i>(Namuna: Abdullayev Abdullajon Abdulla o'g'li)</i>"
        )
        return

    await state.update_data(full_name=message.text)
    await state.set_state(SubmissionState.date_of_birth)

    await message.answer(
        "<b>Tug'ilgan sana va yilingizni kiriting.</b>\n"
        "<i>(Namuna: 31.01.2010)</i>"
    )


@submission_router.message(SubmissionState.date_of_birth, F.text)
async def process_date_of_birth(message: Message, state: FSMContext, repo: RequestsRepo):
    text = message.text
    date_pattern = re.compile('^\d{2}\.\d{2}\.\d{4}$')

    if not re.match(date_pattern, text):
        await message.answer(
            "<b>Tug'ilgan sana va yilni to'g'ri kiriting.</b>\n"
            "<i>(Namuna: 31.01.2010)</i>"
        )
        return
    
    dob = datetime.strptime(text, "%d.%m.%Y").date()
    today = datetime.today().date()
    age = (today - dob).days // 365

    if age < 14:
        await message.answer(
            "<b>Tug'ilgan sana va yilni to'g'ri kiriting.</b>"
        )
        return

    await state.update_data(date_of_birth=message.text)
    await state.set_state(SubmissionState.region)

    regions = await repo.locations.get_regions()
    region_names = [region.name for region in regions]
    keyboard = location_keyboard(region_names)

    await message.answer(
        "<b>Hududingizni tanlang.</b>",
        reply_markup=keyboard
    )


@submission_router.message(SubmissionState.region)
async def process_region(message: Message, state: FSMContext, repo: RequestsRepo):
    regions = await repo.locations.get_regions()
    region_names = [region.name for region in regions]

    if message.text not in region_names:
        keyboard = location_keyboard(region_names)
        await message.answer(
            "<b>Hududni to'g'ri kiriting.</b>",
            reply_markup=keyboard
        )
        return

    await state.update_data(region=message.text)
    await state.set_state(SubmissionState.district)

    districts = await repo.locations.get_districts_by_region_name(message.text)
    district_names = [district.name for district in districts]
    keyboard = location_keyboard(district_names)

    await message.answer(
        "<b>Tuman/shaharni tanlang.</b>",
        reply_markup=keyboard
    )


@submission_router.message(SubmissionState.district)
async def process_district(message: Message, state: FSMContext, repo: RequestsRepo):
    data = await state.get_data()
    mahallas = await repo.locations.get_mahallas_by_district_name(
        message.text,
        data.get("region")
    )
    
    if not mahallas:
        districts = await repo.locations.get_districts_by_region_name(
            data.get("region")
        )
        district_names = [district.name for district in districts]
        keyboard = location_keyboard(district_names)
        await message.answer(
            "<b>Bu hudud uchun faol tuman/shaharlar mavjud emas.</b>",
            reply_markup=keyboard
        )
        return

    await state.update_data(district=message.text)
    await state.set_state(SubmissionState.area)

    mahalla_names = [mahalla.name for mahalla in mahallas]

    keyboard = location_keyboard(mahalla_names)

    await message.answer(
        "<b>Mahallani tanlang.</b>",
        reply_markup=keyboard
    )


@submission_router.message(SubmissionState.area)
async def process_area(message: Message, state: FSMContext, repo: RequestsRepo):
    data = await state.get_data()
    mahalla = await repo.locations.get_mahalla_by_name(
        message.text,
        data.get("district")
    ) 
    if not mahalla:
        mahallas = await repo.locations.get_mahallas_by_district_name(
            data.get("district"),
            data.get("region"),
        )
        mahalla_names = [mahalla.name for mahalla in mahallas]
        keyboard = location_keyboard(mahalla_names)
        await message.answer(
            "<b>Bu tuman/shahar uchun faol mahallalar mavjud emas.</b>",
            reply_markup=keyboard
        )
        return

    await state.update_data(area_id=mahalla.id)
    await state.set_state(SubmissionState.education)

    await message.answer(
        "<b>O'qish joyingizni kiriting.</b>\n"
        "<i>(Namuna: Talaba, O'zMU 2-kurs)</i>",
        reply_markup=ReplyKeyboardRemove()
    )


@submission_router.message(SubmissionState.education)
async def process_education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    await state.set_state(SubmissionState.certificate)

    await message.answer(
        "<b>Soha bo'yicha sertifikatingiz bormi?</b>\n"
        "<i>(PDF formatda, hajmi 10MBdan katta bo'lmagan)</i>",
        reply_markup=skip_keyboard()
    )


@submission_router.message(SubmissionState.certificate, F.document)
async def process_certificate(message: Message, bot: Bot, state: FSMContext):
    document = message.document

    if document.mime_type != 'application/pdf':
        await message.answer(
            "<b>Iltimos, faqat PDF formatdagi fayl yuboring.</b>",
            reply_markup=skip_keyboard()
        )
        return

    if document.file_size > 10 * 1024 * 1024:
        await message.answer(
            "<b>Fayl hajmi 10MBdan katta bo'lmasligi kerak.</b>",
            reply_markup=skip_keyboard()
        )
        return

    file_name = message.document.file_name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    name, ext = os.path.splitext(file_name)
    file_name = f"{name}_{timestamp}{ext}"
    file_path = f"media/uploads/{file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await bot.download(message.document.file_id, file_path)

    await state.update_data(certificate="uploads/" + file_name)
    await state.set_state(SubmissionState.creative_work)

    await message.answer(
        "<b>Ijodiy ishlaringiz bormi?</b>\n"
        "<i>(Havola yuboring)</i>",
        reply_markup=skip_keyboard()
    )


@submission_router.message(SubmissionState.certificate, F.text == "O'tkazib yuborish")
async def process_certificate_skip(message: Message, state: FSMContext):
    await state.update_data(certificate=None)
    await state.set_state(SubmissionState.creative_work)

    await message.answer(
        "<b>Ijodiy ishlaringiz bormi?</b>\n"
        "<i>(Havola yuboring)</i>",
        reply_markup=skip_keyboard()
    )


@submission_router.message(SubmissionState.creative_work, F.text == "O'tkazib yuborish")
async def process_creative_work_skip(message: Message, state: FSMContext):
    await state.update_data(creative_work=None)
    await state.set_state(SubmissionState.photo)

    await message.answer(
        "<b>Rasmingizni yuboring.</b>\n"
        "<i>(9x12 o'lchamda, JPEG formatda)</i>",
        reply_markup=ReplyKeyboardRemove()
    )


@submission_router.message(SubmissionState.creative_work)
async def process_creative_work(message: Message, state: FSMContext):
    await state.update_data(creative_work=message.text)
    await state.set_state(SubmissionState.photo)

    await message.answer(
        "<b>Rasmingizni yuboring.</b>\n"
        "<i>(9x12 o'lchamda, JPEG formatda)</i>",
        reply_markup=ReplyKeyboardRemove()
    )


@submission_router.message(SubmissionState.photo, F.photo)
async def process_photo(message: Message, bot: Bot, state: FSMContext):
    photo = message.photo[-1]

    file_info = await bot.get_file(photo.file_id)
    file_path_ext = os.path.splitext(file_info.file_path)[1].lower()
    if file_path_ext not in [".jpg", ".jpeg"]:
        await message.answer(
            "<b>Iltimos, faqat JPEG formatdagi rasm yuboring.</b>"
        )
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f"{message.from_user.id}_{timestamp}{file_path_ext}"
    file_path = f"media/images/{file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await bot.download(photo.file_id, file_path)

    await state.update_data(photo="images/" + file_name)
    await state.set_state(SubmissionState.phone_number)

    button = KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        "<b>Telefon raqamingizni yuboring.</b>",
        reply_markup=keyboard
    )


@submission_router.message(SubmissionState.phone_number, F.contact)
async def process_phone_number(
    message: Message,
    state: FSMContext,
    repo: RequestsRepo,
    user: TgUser,
):
    contact = message.contact
    await state.update_data(phone_number=contact.phone_number)
    data = await state.get_data()

    submission = await repo.submissions.create_submission(
        tg_user_id=user.id,
        full_name=data["full_name"],
        date_of_birth=datetime.strptime(data["date_of_birth"], "%d.%m.%Y").date(),
        area_id=data["area_id"],
        photo=data["photo"],
        education=data["education"],
        certificate=data["certificate"],
        creative_work=data["creative_work"],
        phone_number=data["phone_number"]
    )
    logging.info(
        f"New submission created: {submission.id} by user {message.from_user.id}"
    )

    await message.answer(
        "<b>Ma'lumotlaringiz qabul qilindi!</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()
