from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from datetime import datetime
import logging
import os
import psycopg2
from html import escape

from config import bot, scheduler, reminders
from keyboards.main import (
    get_reminders_menu,
    get_delete_reminder_keyboard,
    get_cancel_keyboard,
    get_main_menu
)
from states import Form

router = Router()
logger = logging.getLogger(__name__)

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

        # Сохраняем в PostgreSQL
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (user_id, text, time, active) VALUES (%s, %s, %s, %s) RETURNING id",
            (user_id, escape(data["text"]), time.strftime("%H:%M"), True)
        )
        reminder_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

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
    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")
        await message.answer("❌ Ошибка при сохранении!")

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
@router.callback_query(F.data.startswith("delete_"))
async def delete_reminder(callback: CallbackQuery):
    try:
        # Получаем ID напоминания
        _, reminder_id_str = callback.data.split("_")
        reminder_id = int(reminder_id_str)
        user_id = callback.from_user.id

        # Удаление из PostgreSQL
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM reminders WHERE id = %s AND user_id = %s",
            (reminder_id, user_id)
        )
        conn.commit()
        conn.close()

        # Удаление из планировщика
        scheduler.remove_job(f"reminder_{user_id}_{reminder_id}")

        # Обновление локального кэша
        if user_id in reminders:
            reminders[user_id] = [
                rem for rem in reminders[user_id]
                if rem["id"] != reminder_id
            ]

        await callback.message.answer("✅ Напоминание удалено!")
    except (ValueError, IndexError):
        await callback.answer("⚠️ Неверный формат команды!")
    except Exception as e:
        logger.error(f"Ошибка удаления: {e}")
        await callback.answer("❌ Ошибка при удалении!")
    finally:
        await callback.answer()

# Отправка уведомления
async def send_reminder(user_id: int, text: str):
    try:
        await bot.send_message(user_id, f"🔔 Напоминание: {text}")
        logger.info(f"Отправлено напоминание пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")

# Общая отмена
@router.message(F.text == "❌ Отмена")
async def cancel_action(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=get_main_menu())