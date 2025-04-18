from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from config import HEALTH_TIPS
from keyboards.main import get_health_tips_menu, get_back_to_tips_keyboard

router = Router()


@router.message(F.text == "💡 Советы")
async def health_tips_menu(message: Message):
    await message.answer(
        "📚 <b>Выберите категорию советов:</b>",
        reply_markup=get_health_tips_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("tips_"))
async def send_tips(callback: CallbackQuery):
    category = callback.data.split("_")[1]
    tips = HEALTH_TIPS.get(category, [])

    text = f"🔍 <b>Советы ({category.capitalize()}):</b>\n\n" + "\n\n".join(tips)
    await callback.message.edit_text(  # Редактируем сообщение вместо отправки нового
        text,
        parse_mode="HTML",
        reply_markup=get_back_to_tips_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_tips")
async def back_to_tips_menu(callback: CallbackQuery):
    await callback.message.edit_text(  # Редактируем текущее сообщение
        "📚 <b>Выберите категорию советов:</b>",
        parse_mode="HTML",
        reply_markup=get_health_tips_menu()
    )
    await callback.answer()