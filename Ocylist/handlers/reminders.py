from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from datetime import datetime
from keyboards.main import (
    get_reminders_menu,
    get_delete_reminder_keyboard,
    get_cancel_keyboard,
    get_main_menu
)
from config import bot, scheduler, reminders
from states import Form
import sqlite3
from html import escape

router = Router()


# Меню напоминаний
@router.message(F.text == "⏰ Напоминания")
async def reminders_menu(message: Message):
    await message.answer(
        "⏰ Управление напоминаниями:",
        reply_markup=get_reminders_menu()
    )


# Добавление напоминания (шаг 1: текст)
@router.callback_query(F.data == "add_reminder")
async def add_reminder_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📝 Введите текст напоминания (например: 'Закапать капли'):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Form.waiting_for_reminder_text)
    await callback.answer()


# Шаг 2: время
@router.message(Form.waiting_for_reminder_text)
async def process_reminder_text(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_action(message, state)
        return

    await state.update_data(text=message.text)
    await message.answer(
        "⏰ Введите время в формате ЧЧ:ММ (например: 15:30):",
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(Form.waiting_for_reminder_time)


# Сохранение напоминания
@router.message(Form.waiting_for_reminder_time)
async def process_reminder_time(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await cancel_action(message, state)
        return

    try:
        data = await state.get_data()
        time = datetime.strptime(message.text, "%H:%M").time()
        user_id = message.from_user.id

        # Сохраняем в БД
        with sqlite3.connect('bot_data.db') as conn:
            cursor = conn.execute(
                "INSERT INTO reminders (user_id, text, time, active) VALUES (?, ?, ?, ?)",
                (user_id, escape(data["text"]), time.strftime("%H:%M"), True)
            )
            reminder_id = cursor.lastrowid

        # Добавляем в планировщик
        scheduler.add_job(
            send_reminder,
            trigger="cron",
            hour=time.hour,
            minute=time.minute,
            args=(user_id, data["text"]),
            id=f"reminder_{user_id}_{reminder_id}"
        )

        # Обновляем локальный список
        if user_id not in reminders:
            reminders[user_id] = []
        reminders[user_id].append({
            "id": reminder_id,
            "text": data["text"],
            "time": time,
            "active": True
        })

        await message.answer(
            f"✅ Напоминание установлено на {time.strftime('%H:%M')}!",
            reply_markup=get_main_menu()
        )
        await state.clear()

    except ValueError:
        await message.answer("❌ Неверный формат времени!")


# Список напоминаний
@router.callback_query(F.data == "list_reminders")
async def list_reminders(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_reminders = reminders.get(user_id, [])

    if not user_reminders:
        await callback.message.answer("📭 У вас нет напоминаний.")
    else:
        text = "📋 Ваши напоминания:\n\n"
        for idx, rem in enumerate(user_reminders, 1):
            status = "✅ Активно" if rem["active"] else "❌ Выключено"
            text += f"{idx}. {rem['text']} в {rem['time'].strftime('%H:%M')} ({status})\n"

        await callback.message.answer(text)
    await callback.answer()


# Удаление напоминаний
@router.callback_query(F.data == "delete_reminder")
async def delete_reminder_menu(callback: CallbackQuery):
    await callback.message.answer(
        "🗑 Выберите напоминание для удаления:",
        reply_markup=get_delete_reminder_keyboard(callback.from_user.id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("delete_"))
async def delete_reminder(callback: CallbackQuery):
    user_id = callback.from_user.id
    idx = int(callback.data.split("_")[1])

    if user_id not in reminders or idx >= len(reminders[user_id]):
        await callback.answer("⚠️ Напоминание не найдено!")
        return

    try:
        reminder = reminders[user_id].pop(idx)
        # Удаляем из БД
        with sqlite3.connect('bot_data.db') as conn:
            conn.execute(
                "DELETE FROM reminders WHERE id = ? AND user_id = ?",
                (reminder["id"], user_id)
            )
        # Удаляем из планировщика
        scheduler.remove_job(f"reminder_{user_id}_{reminder['id']}")
        await callback.message.answer("✅ Напоминание удалено!")
    except Exception as e:
        await callback.message.answer("❌ Ошибка при удалении!")
    await callback.answer()


# Отправка уведомления
async def send_reminder(user_id: int, text: str):
    await bot.send_message(user_id, f"🔔 Напоминание: {text}")


# Общая отмена
@router.message(F.text == "❌ Отмена")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_main_menu())