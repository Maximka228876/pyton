from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.main import get_help_menu, get_main_menu

router = Router()

HELP_TEXT = (
    "🆘 <b>Помощь по боту:</b>\n\n"
    "1. 👁️ Проверить зрение — тесты для самодиагностики.\n"
    "2. 💡 Советы — рекомендации по здоровью глаз.\n"
    "3. 🤒 Заболевания — информация о глазных заболеваниях.\n"
    "4. 🏥 Запись к врачу — контакты клиник.\n\n"
    "⚠️ Если возникла ошибка, напишите сюда: @Hihihigrrr"
)

@router.message(F.text == "❓ Помощь")
async def help_command(message: Message):
    await message.answer(
        HELP_TEXT,
        parse_mode="HTML",
        reply_markup=get_help_menu()
    )

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()
