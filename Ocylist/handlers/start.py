import psycopg2
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.db import init_db
from keyboards.main import get_main_menu
import os
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (user_id, first_name, last_name, username, reg_date) "
            "VALUES (%s, %s, %s, %s, NOW()) "
            "ON CONFLICT (user_id) DO NOTHING",
            (user.id, user.first_name, user.last_name, user.username)
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Ошибка при регистрации пользователя: {e}")
    finally:
        conn.close()
    
    await message.answer(f"👋 Привет, {user.first_name}! Я бот-окулист!", reply_markup=get_main_menu())
