from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart
# import sqlite3

import asyncio
import logging

from config_reader import config
from handlers.add_report import add_report_router
# from handlers.get_report_money import get_report_money_router
from handlers.add_employee import add_employee_router
from handlers.delete_employee import delete_employee_router
# from handlers.get_employee_report import get_employee_report_router
from handlers.add_employee_quests import add_employee_quests_router

logging.basicConfig(level=logging.INFO)
# connection = sqlite3.connect("./database/database.db")
# cursor = connection.cursor()
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

dp.include_router(add_report_router)
dp.include_router(add_employee_router)
# dp.include_router(get_report_money_router)
dp.include_router(delete_employee_router)
# dp.include_router(get_employee_report_router)
dp.include_router(add_employee_quests_router)

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Reports (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     тип_смены type TEXT NOT NULL,
#     дата type DATE NOT NULL,
#     админ type TEXT,
#     эвотор_нал type FLOAT NOT NULL,
#     эвотор_безнал type FLOAT NOT NULL,
#     лангейм_нал type FLOAT NOT NULL,
#     терминал_нал type FLOAT NOT NULL,
#     терминал_безнал type FLOAT NOT NULL,
#     терминал_сбп type FLOAT NOT NULL,
#     возврат_эвотор type FLOAT ,
#     возврат_лангейм type FLOAT ,
#     итого type FLOAT NOT NULL
# )
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Employees (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     тип_смены type TEXT NOT NULL,
#     имя type TEXT NOT NULL,
#     номер_телефона type INTEGER
# )
# """)
#
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS EmployeesReports (
#     id INTEGER  PRIMARY KEY AUTOINCREMENT,
#     админ type TEXT NOT NULL,
#     количество_смен type INTEGER,
#     дата type DATE,
#     задачи type TEXT
# )
# """)
#
# connection.commit()
# connection.close()

@add_report_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("⬇️Используйте меню для выбора команды")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
