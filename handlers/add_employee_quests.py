from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from database.database import db_get_employee

add_employee_quests_router = Router()


class AddEmployeeQuests(StatesGroup):
    employee = State()
    quest = State()


@add_employee_quests_router.message(Command("addemployeequests"))
async def cmd_add_employee_quests(message: types.Message, state: FSMContext):
    await state.set_state(AddEmployeeQuests.employee)

    rows = db_get_employee()
    builder = ReplyKeyboardBuilder()
    for row in rows:
        builder.add(types.KeyboardButton(text=row[0]))
    builder.adjust(2)

    await message.answer(
        "Укажите админа",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
    )


@add_employee_quests_router.message(AddEmployeeQuests.employee)
async def add_employee_quests_employee(message: types.Message, state: FSMContext):
    await state.update_data(employee=message.text)
    await state.set_state(AddEmployeeQuests.quest)
    await message.answer("Укажите выполнение задачи")


@add_employee_quests_router.message(AddEmployeeQuests.quest)
async def add_employee_quests_quest(message: types.Message, state: FSMContext):
    await state.update_data(quest=message.text)
    await state.clear()
