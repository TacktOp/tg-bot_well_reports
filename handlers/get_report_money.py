from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import datetime

from database.database import db_get_report_money

get_report_money_router = Router()


class GetReportMoney(StatesGroup):
    date = State()


@get_report_money_router.message(Command("getreportmoney"))
async def cmd_get_report_money(message: types.Message, state: FSMContext):
    await state.set_state(GetReportMoney.date)
    await message.answer(
        "Укажите даты для итогов отчётов\n\n"
        "Пример:\n"
        "05-29 по 05-30"
    )


@get_report_money_router.message(GetReportMoney.date)
async def get_report_money(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    dates = f'{data["date"]}'.replace("по", "").split()
    await message.answer(db_get_report_money(dates))
