from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main import get_diseases_menu, get_back_to_diseases_keyboard

router = Router()

DISEASES_INFO = {
    "myopia": {
        "title": "🔍 Близорукость (Миопия)",
        "content": (
            "• Причины: генетика, длительная работа на близком расстоянии\n"
            "• Симптомы: размытое зрение вдали, прищуривание\n"
            "• Лечение: очки, линзы, лазерная коррекция"
        )
    },
    "cataract": {
        "title": "🌀 Катаракта",
        "content": (
            "• Причины: возраст, травмы, диабет\n"
            "• Симптомы: помутнение хрусталика, блики\n"
            "• Лечение: замена хрусталика хирургически"
        )
    }
}

@router.message(F.text == "👁️ Заболевания")
async def diseases_menu(message: Message):
    await message.answer(
        "📚 Выберите заболевание:",
        reply_markup=get_diseases_menu()
    )

@router.callback_query(F.data.startswith("disease_"))
async def show_disease_info(callback: CallbackQuery):
    disease_key = callback.data.split("_")[1]
    disease = DISEASES_INFO.get(disease_key)
    
    if not disease:
        await callback.answer("⚠️ Информация отсутствует")
        return

    text = f"<b>{disease['title']}</b>\n\n{disease['content']}"
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_back_to_diseases_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_diseases")
async def back_to_diseases_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 Выберите заболевание:",
        reply_markup=get_diseases_menu()
    )
    await callback.answer()
