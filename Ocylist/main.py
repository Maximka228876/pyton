import asyncio
import logging
import datetime
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from config import dp, bot, scheduler
from handlers.reminders import load_reminders_on_startup
from database.db import init_db  # Добавлен импорт

# Импорт роутеров
from handlers.start import router as start_router
from handlers.vision import router as vision_router
from handlers.reminders import router as reminders_router
from handlers.feedback import router as feedback_router
from handlers.common import router as common_router
from handlers.clinics import router as clinics_router
from handlers.tips import router as tips_router
from handlers.help import router as help_router

load_dotenv()

async def on_startup():
    """Действия при запуске бота"""
    init_db()  # Инициализация БД
    await load_reminders_on_startup()
    logging.info("Напоминания загружены")
    server_time = datetime.datetime.now()
    logging.info(f"Текущее время сервера: {server_time}")
    logging.info(f"Часовой пояс сервера: {server_time.astimezone().tzinfo}")

async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(vision_router)
    dp.include_router(reminders_router)
    dp.include_router(feedback_router)
    dp.include_router(common_router)
    dp.include_router(clinics_router)
    dp.include_router(tips_router)
    dp.include_router(help_router)

    # Запуск планировщика
    if not scheduler.running:
        scheduler.start()
        logging.info("Планировщик запущен")

    # Стартовые задачи
    await on_startup()

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
