from aiogram import Bot, Dispatcher
import sqlite3

import asyncio
import logging

from config_reader import config
from handlers.reports import reports_router

logging.basicConfig(level=logging.INFO)
connection = sqlite3.connect("./database/database.db")
cursor = connection.cursor()
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

dp.include_router(reports_router)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    тип_смены type TEXT NOT NULL,
    дата type DATE NOT NULL,
    админ_дневной type TEXT,
    админ_ночной type TEXT,
    админ_промежуточный type TEXT,
    эвотор_нал type INTEGER NOT NULL,
    эвотор_безнал type INTEGER NOT NULL,
    лангейм_нал type INTEGER NOT NULL,
    лангейм_безанл type INTEGER NOT NULL,
    возврат_эвотор type INTEGER,
    возврат_лангейм type INTEGER,
    итого type INTEGER NOT NULL
)
""")

connection.commit()
connection.close()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
