from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import datetime

from database.database import db_add_report

add_report_router = Router()


class AddReport(StatesGroup):
    money = State()
    employee = State()
    returns_money = State()


@add_report_router.message(Command("addnewreport"))
async def cmd_add_report_money(message: types.Message, state: FSMContext):
    await state.set_state(AddReport.money)
    await message.answer(
        "Введите нал/общая за эвотор и нал/безнал/сбп за лангейм/терминал\n\n"
        "Пример:\n"
        "1000 (нал эвотор)\n"
        "2000 (объщая сумма эвотор)\n"
        "1000 (нал лангейм)\n"
        "2000 (нал терминал)\n"
        "3000 (безнал терминал)\n"
        "4000 (сбп терминал)\n"
    )


@add_report_router.message(AddReport.money)
async def add_report_name(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await state.set_state(AddReport.employee)
    await message.answer(
        "Укажите админа\n\n"
        "Пример:\n"
        "Слава\n"
    )


@add_report_router.message(AddReport.employee)
async def add_report_returns(message: types.Message, state: FSMContext):
    await state.update_data(employee=message.text)
    await state.set_state(AddReport.returns_money)
    await message.answer(
        "Укажите возвраты за эвотор и лангейм\n\n"
        "Пример:\n"
        "123 (эвотор, если нет пиши 0)\n"
        "123 (лангейм, если нет пиши 0)"
    )


@add_report_router.message(AddReport.returns_money)
async def add_report(message: types.Message, state: FSMContext):
    await state.update_data(returns_money=message.text)
    data = await state.get_data()
    await state.clear()
    moneys = f"{data['money']}".replace("\n", " ").split()
    employee = data['employee']
    returns = f"{data['returns_money']}".replace("\n", " ").split()
    total = int(moneys[1]) + int(moneys[2]) + int(moneys[3]) + int(moneys[4]) + int(moneys[5])
    if datetime.datetime.now().hour >= 20 and datetime.datetime.now().hour <= 23:
        db_add_report(
            'день',
            datetime.datetime.now().date(),
            employee,
            int(moneys[0]),
            int(moneys[1]) - int(moneys[0]),
            int(moneys[2]),
            int(moneys[3]),
            int(moneys[4]),
            int(moneys[5]),
            int(returns[0]),
            int(returns[1]),
            total
        )
        await message.answer(
            f"Дневная смена администратор:\n"
            f"{employee}\n\n"
            f"{datetime.datetime.now().date()}\n\n"
            f"Эватор:\n"
            f"Нал {moneys[0]}₽\n"
            f"Безнал {int(moneys[1]) - int(moneys[0])}₽\n"
            f"Возврат {int(returns[0])}₽\n\n"
            f"Лангейм:\n"
            f"Нал {moneys[2]}₽\n\n"
            f"Терминал:\n"
            f"Нал {moneys[3]}₽\n"
            f"Безнал {moneys[4]}₽\n"
            f"СБП {moneys[5]}₽\n\n"
            f"Возврат {int(returns[1])}₽\n\n"
            f"Возвраты: {int(returns[0]) + int(returns[1])}₽\n"
            f"Итого: {total}₽"
        )

    elif datetime.datetime.now().hour >= 9 and datetime.datetime.now().hour <= 11:
        db_add_report(
            'ночь',
            datetime.datetime.today().date() - datetime.timedelta(days=1),
            employee,
            int(moneys[0]),
            int(moneys[1]) - int(moneys[0]),
            int(moneys[2]),
            int(moneys[3]),
            int(moneys[4]),
            int(moneys[5]),
            int(returns[0]),
            int(returns[1]),
            total
        )
        await message.answer(
            f"Ночная смена администратор:\n"
            f"{employee}\n\n"
            f"{datetime.datetime.today().date() - datetime.timedelta(days=1)}\n\n"
            f"Эватор:\n"
            f"Нал {moneys[0]}₽\n"
            f"Безнал {int(moneys[1]) - int(moneys[0])}₽\n"
            f"Возврат {int(returns[0])}₽\n\n"
            f"Лангейм:\n"
            f"Нал {moneys[2]}₽\n"
            f"Терминал:\n"
            f"Нал {moneys[3]}₽\n"
            f"Безнал {moneys[4]}₽\n"
            f"СБП {moneys[5]}₽\n\n"
            f"Возврат {int(returns[1])}₽\n\n"
            f"Возвраты: {int(returns[0]) + int(returns[1])}₽\n"
            f"Итого: {total}₽"
        )
