from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.main import get_main_menu

router = Router()

@router.callback_query(F.data == "back_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "Главное меню:",
        reply_markup=get_main_menu()
    )
    await callback.answer()