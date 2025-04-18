import sqlite3
from datetime import datetime
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database.db import init_db
from keyboards.main import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    with sqlite3.connect('bot_data.db') as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)",
            (user.id, user.first_name, user.last_name, user.username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
    await message.answer(f"👋 Привет, {user.first_name}! Я бот-окулист!", reply_markup=get_main_menu())