from aiogram import types, Router
from aiogram.filters.command import Command

from database.database import db_get_employee_report

get_employee_report_router = Router()

@get_employee_report_router.message(Command("getemployeereport"))
async def cmd_get_employee_report(message: types.Message):
    data = db_get_employee_report()
    await message.answer(data)
