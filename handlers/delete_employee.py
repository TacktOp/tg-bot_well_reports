from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.database import db_delete_employee

delete_employee_router = Router()


class DeleteEmployee(StatesGroup):
    datas = State()


@delete_employee_router.message(Command("deleteemployee"))
async def cmd_delete_employee(message: types.Message, state: FSMContext):
    await state.set_state(DeleteEmployee.datas)
    await message.answer(
        "Укажите имя и номер телефона сотрудника\n\n"
        "Пример:\n"
        "Аркадий\n"
        "79825109054"
    )


@delete_employee_router.message(DeleteEmployee.datas)
async def delete_employee(message: types.Message, state: FSMContext):
    await state.update_data(datas=message.text)
    data = await state.get_data()
    await state.clear()
    data = f"{data['datas']}".replace("\n", " ").split()
    result = db_delete_employee(data[0], data[1])
    if result == False:
        await message.answer("Данные не найдены")
    else:
        await message.answer("Сотудник удалён")
