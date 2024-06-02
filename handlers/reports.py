from aiogram import types, Router
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import datetime

from database.database import db_add_new_report, db_get_report_money

reports_router = Router()


class AddNewReport(StatesGroup):
    money = State()
    employee = State()
    returns_money = State()


class GetReportMoney(StatesGroup):
    date = State()


@reports_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Используйте меню для выбора команды")


@reports_router.message(Command("addnewreport"))
async def cmd_add_new_report_money(message: types.Message, state: FSMContext):
    await state.set_state(AddNewReport.money)
    await message.answer(
        "Введите нал/объщая за эвотор и нал/безнал за лангейм\n\n"
        "Пример:\n"
        "1234 (нал эвотор)\n"
        "4321 (объщая сумма эвотор)\n"
        "1234 (нал лангейм)\n"
        "4321 (безнал лангейм)"
    )


@reports_router.message(Command("getreportmoney"))
async def cmd_get_report_money(message: types.Message, state: FSMContext):
    await state.set_state(GetReportMoney.date)
    await message.answer(
        "Укажите даты для итогов отчётов\n\n"
        "Пример:\n"
        "05-29 по 05-30"
    )


@reports_router.message(AddNewReport.money)
async def add_new_report_name(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await state.set_state(AddNewReport.employee)
    await message.answer(
        "Укажите дневного, ночного и промежуточного админа\n\n"
        "Пример:\n"
        "Слава (дневной)\n"
        "Ваня (ночной)\n"
        "Артём (промежуточного)\n"
    )


@reports_router.message(AddNewReport.employee)
async def add_new_report_returns(message: types.Message, state: FSMContext):
    await state.update_data(employee=message.text)
    await state.set_state(AddNewReport.returns_money)
    await message.answer(
        "Укажите возвраты за эвотор и лангейм\n\n"
        "Пример:\n"
        "123 (эвотор, если нет пиши 0)\n"
        "123 (лангейм, если нет пиши 0)"
    )


@reports_router.message(AddNewReport.returns_money)
async def add_new_report(message: types.Message, state: FSMContext):
    await state.update_data(returns_money=message.text)
    data = await state.get_data()
    moneys = f"{data['money']}".replace("\n", " ").split()
    employees = f"{data['employee']}".replace("\n", " ").split()
    returns = f"{data['returns_money']}".replace("\n", " ").split()
    if datetime.datetime.now().hour >= 20 and datetime.datetime.now().hour <= 23:
        db_add_new_report(
            'день',
            datetime.datetime.now().date(),
            employees[0],
            employees[1],
            employees[2],
            int(moneys[0]),
            int(moneys[1]) - int(moneys[0]),
            int(moneys[2]),
            int(moneys[3]),
            int(returns[0]),
            int(returns[1]),
            (int(moneys[1]) + int(moneys[2]) + int(moneys[3])) - (int(returns[0]) + int(returns[1]))
        )
        await message.answer(
            f"Дневная смена администратор:\n"
            f"{employees[0]}\n\n"
            f"Промежуточный администратор:\n"
            f"{employees[2]}\n\n"
            f"{datetime.datetime.now().date()}\n\n"
            f"Эватор:\n"
            f"Нал {moneys[0]}₽\n"
            f"Безнал {int(moneys[1]) - int(moneys[0])}₽\n"
            f"Возврат {int(returns[0])}₽\n\n"
            f"Лангейм:\n"
            f"Нал {moneys[2]}₽\n"
            f"Безнал {moneys[3]}₽\n"
            f"Возврат {int(returns[1])}₽\n\n"
            f"Возвраты: {int(returns[0]) + int(returns[1])}₽\n"
            f"Итого: {(int(moneys[1]) + int(moneys[2]) + int(moneys[3])) - (int(returns[0]) + int(returns[1]))}₽"
        )

    elif datetime.datetime.now().hour >= 9 and datetime.datetime.now().hour <= 11:
        db_add_new_report(
            'ночь',
            datetime.datetime.today().date() - datetime.timedelta(days=1),
            employees[0],
            employees[1],
            employees[2],
            int(moneys[0]),
            int(moneys[1]) - int(moneys[0]),
            int(moneys[2]),
            int(moneys[3]),
            int(returns[0]),
            int(returns[1]),
            (int(moneys[1]) + int(moneys[2]) + int(moneys[3])) - (int(returns[0]) + int(returns[1]))
        )
        await message.answer(
            f"Ночная смена администратор:\n"
            f"{employees[1]}\n\n"
            f"Промежуточный администратор:\n"
            f"{employees[2]}\n\n"
            f"{datetime.datetime.today().date() - datetime.timedelta(days=1)}\n\n"
            f"Эватор:\n"
            f"Нал {moneys[0]}₽\n"
            f"Безнал {int(moneys[1]) - int(moneys[0])}₽\n"
            f"Возврат {int(returns[0])}₽\n\n"
            f"Лангейм:\n"
            f"Нал {moneys[2]}₽\n"
            f"Безнал {moneys[3]}₽\n"
            f"Возврат {int(returns[1])}₽\n\n"
            f"Возвраты: {int(returns[0]) + int(returns[1])}₽\n"
            f"Итого: {(int(moneys[1]) + int(moneys[2]) + int(moneys[3])) - (int(returns[0]) + int(returns[1]))}₽"
        )


@reports_router.message(GetReportMoney.date)
async def get_report_money(message: types.Message, state: FSMContext):
    await state.update_data(date=message.text)
    data = await state.get_data()
    dates = f'{data["date"]}'.replace("по", "").split()
    await message.answer(db_get_report_money(dates))
