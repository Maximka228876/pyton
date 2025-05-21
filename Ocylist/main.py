import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from config import dp, bot, scheduler
from database.db import init_db

from handlers.diseases import router as diseases_router
from handlers.start import router as start_router
from handlers.vision import router as vision_router
from handlers.feedback import router as feedback_router
from handlers.common import router as common_router
from handlers.clinics import router as clinics_router
from handlers.tips import router as tips_router
from handlers.help import router as help_router

load_dotenv()

async def on_startup():
    init_db()
    logging.info("Бот запущен")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    dp.include_router(diseases_router)
    dp.include_router(start_router)
    dp.include_router(vision_router)
    dp.include_router(feedback_router)
    dp.include_router(common_router)
    dp.include_router(clinics_router)
    dp.include_router(tips_router)
    dp.include_router(help_router)

    if not scheduler.running:
        scheduler.start()
        logging.info("Планировщик запущен")

    await on_startup()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
