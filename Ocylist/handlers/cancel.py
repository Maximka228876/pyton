from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards.main import get_main_menu

router = Router()

@router.message(F.text == "❌ Отмена")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "❌ Действие отменено",
        reply_markup=get_main_menu()
    )