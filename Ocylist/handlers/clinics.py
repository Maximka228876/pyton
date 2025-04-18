from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup
from config import CLINICS
from keyboards.main import get_clinics_menu

router = Router()

@router.message(F.text == "🏥 Запись к врачу")
async def clinics_list(message: Message):
    text = "🏥 Список клиник:\n\n"
    for clinic in CLINICS:
        text += (
            f"{clinic['name']}\n"
            f"📍 Адрес: {clinic['address']}\n"
            f"📞 Телефон: {clinic['phone']}\n"
            f"🌐 Сайт: {clinic['website']}\n\n"
        )
    await message.answer(
        text,
        disable_web_page_preview=True,
        reply_markup=get_clinics_menu()
    )