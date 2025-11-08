from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
# from aiogram.utils.keyboard import ReplyKeyboardBuilder

import datetime

# from database.database import db_add_report, db_get_employee, db_update_employee_report

add_report_router = Router()


class AddReport(StatesGroup):
    money = State()
    employee = State()
    bonuses = State()
    info_bonuses = State()
    returns_money = State()
    steam = State()


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
        "1000 (сбп планшет)\n"
    )


@add_report_router.message(AddReport.money)
async def add_report_name(message: types.Message, state: FSMContext):
    await state.update_data(money=message.text)
    await state.set_state(AddReport.employee)

    # rows = db_get_employee()
    #
    # builder = ReplyKeyboardBuilder()
    # for row in rows:
    #     builder.add(types.KeyboardButton(text=row[0]))
    # builder.adjust(2)

    await message.answer(
        "Укажите админа")
    #     ,reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    # )


@add_report_router.message(AddReport.employee)
async def add_report_returns(message: types.Message, state: FSMContext):
    await state.update_data(employee=message.text)
    # db_update_employee_report(message.text)
    await state.set_state(AddReport.returns_money)
    await message.answer(
        "Укажите возвраты за эвотор И лангейм\n\n"
        "Пример:\n"
        "100 ('эвотор', если нет пиши 0)\n"
        "200 ('лангейм', если нет пиши 0)"
    )


@add_report_router.message(AddReport.returns_money)
async def add_report_bonuses(message: types.Message, state: FSMContext):
    await state.update_data(returns_money=message.text)
    await state.set_state(AddReport.bonuses)
    await message.answer(
        "Укажите пополнения бонусов\n\n"
        "Пример:\n"
        "10\n"
        "20\n"
        "100\n"
    )


@add_report_router.message(AddReport.bonuses)
async def add_report_info_bonuses(message: types.Message, state: FSMContext):
    await state.update_data(bonuses=message.text)
    await state.set_state(AddReport.info_bonuses)
    await message.answer(
        "Укажите причину пополнение бонусов\n"
        "Пример:\n"
        "Обновление Фортнайт"
    )


@add_report_router.message(AddReport.info_bonuses)
async def add_report_steam(message: types.Message, state: FSMContext):
    await state.update_data(info_bonuses=message.text)
    await state.set_state(AddReport.steam)
    await message.answer("Укажите количество проданых аккаунтов Steam")


@add_report_router.message(AddReport.steam)
async def add_report(message: types.Message, state: FSMContext):
    await state.update_data(steam=message.text)
    data = await state.get_data()
    await state.clear()
    moneys = f"{data['money']}".replace("\n", " ").replace(",", ".").split()
    employee = data['employee']
    bonuses = f"{data['bonuses']}".replace("\n", " ").split()
    bonuses_x = 0
    bonuses_summ = 0
    for bonuses_i in bonuses:
        bonuses_x += 1
        bonuses_summ += int(bonuses_i)
    info_bonuses = data['info_bonuses']

    returns = f"{data['returns_money']}".replace("\n", " ").split()
    if returns[1] is None:
        returns[1] = '0'

    steam = int(data['steam'])
    steam_summ = steam * 150

    total = float(
        moneys[1]) + float(moneys[2]) + float(moneys[3]) + float(moneys[4]) + float(moneys[5]) + float(moneys[6])

    if datetime.datetime.now().hour >= 0:
        # db_add_report(
        #     'день',
        #     datetime.datetime.now().date(),
        #     employee,
        #     float(moneys[0]),
        #     float(moneys[1]) - float(moneys[0]),
        #     float(moneys[2]),
        #     float(moneys[3]),
        #     float(moneys[4]),
        #     float(moneys[5]),
        #     float(returns[0]),
        #     float(returns[1]),
        #     total
        # )

        await message.answer(
            f"Дневная смена администратор:\n"
            f"{employee}\n\n"
            f"{datetime.datetime.now().date()}\n\n"
            f"Эватор:\n"
            f"Нал {moneys[0]}₽\n"
            f"Безнал {float(moneys[1]) - float(moneys[0])}₽\n"
            f"Возврат {float(returns[0])}₽\n\n"
            f"Лангейм:\n"
            f"Нал {moneys[2]}₽\n\n"
            f"Терминал:\n"
            f"Нал {moneys[3]}₽\n"
            f"Безнал {moneys[4]}₽\n"
            f"СБП {moneys[5]}₽\n"
            f"Возврат {float(returns[1])}₽\n\n"
            f"Планшет:\n"
            f"СБП {moneys[6]}"
            f"Бонусы:\n"
            f"Сумма {bonuses_summ}\n"
            f"Кол-во пополнений {bonuses_x}\n\n"
            f"Причина: {info_bonuses}"
            f"Возвраты: {float(returns[0]) + float(returns[1])}₽\n"
            f"Итого: {total}₽"
        )

    elif 9 <= datetime.datetime.now().hour <= 11:
        # db_add_report(
        #     'ночь',
        #     datetime.datetime.today().date() - datetime.timedelta(days=1),
        #     employee,
        #     float(moneys[0]),
        #     float(moneys[1]) - float(moneys[0]),
        #     float(moneys[2]),
        #     float(moneys[3]),
        #     float(moneys[4]),
        #     float(moneys[5]),
        #     float(returns[0]),
        #     float(returns[1]),
        #     total
        # )
        await message.answer(
            f"Ночная смена администратор:\n"
            f"{employee}\n\n"
            f"{datetime.datetime.now().date()}\n\n"
            f"Эватор:\n"
            f"Нал {moneys[0]}₽\n"
            f"Безнал {float(moneys[1]) - float(moneys[0])}₽\n"
            f"Возврат {float(returns[0])}₽\n\n"
            f"Лангейм:\n"
            f"Нал {moneys[2]}₽\n\n"
            f"Терминал:\n"
            f"Нал {moneys[3]}₽\n"
            f"Безнал {moneys[4]}₽\n"
            f"СБП {moneys[5]}₽\n"
            f"Возврат {float(returns[1])}₽\n\n"
            f"Планшет:\n"
            f"СБП {moneys[6]}"
            f"Бонусы:\n"
            f"Сумма {bonuses_summ}\n"
            f"Кол-во пополнений {bonuses_x}\n\n"
            f"Причина: {info_bonuses}"
            f"Возвраты: {float(returns[0]) + float(returns[1])}₽\n"
            f"Итого: {total}₽"
        )
