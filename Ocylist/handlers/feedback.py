from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import bot
from states import Form
from keyboards.main import get_main_menu, get_cancel_keyboard
from html import escape
import logging

router = Router()

# ID чата, куда отправляются отзывы
FEEDBACK_CHAT_ID = -1002523164911  # Именно этот ID из вашего JSON

# Запуск ввода отзыва
@router.message(F.text == "📝 Оставить отзыв")
async def feedback_menu(message: Message, state: FSMContext):
    await message.answer(
        "💬 Напишите ваш отзыв:",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Form.waiting_for_feedback)


# Обработка отзыва
@router.message(Form.waiting_for_feedback)
async def process_feedback(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_action(message, state)
        return

    feedback_text = escape(message.text)
    user = message.from_user
    success = False

    # Формируем информацию о пользователе
    user_info = []
    if user.username:
        user_info.append(f"@{user.username}")
    if user.first_name:
        user_info.append(user.first_name)
    if user.last_name:
        user_info.append(user.last_name)

    # Если нет никаких данных, используем ID
    if not user_info:
        user_info.append(f"ID: {user.id}")

    user_display = " ".join(user_info)

    try:
        await bot.send_message(
            FEEDBACK_CHAT_ID,
            f"📝 Отзыв от {user_display}:\n{feedback_text}"
        )
        success = True
    except Exception as e:
        logging.error(f"Ошибка отправки отзыва: {e}")

    if success:
        await message.answer("✅ Спасибо за отзыв!", reply_markup=get_main_menu())
    else:
        await message.answer(
            "❌ Не удалось отправить отзыв. Попробуйте позже.",
            reply_markup=get_main_menu()
        )
    await state.clear()

# Обработчик отмены
@router.message(F.text == "❌ Отмена")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_main_menu())