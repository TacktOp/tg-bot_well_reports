from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import db_add_employee

add_employee_router = Router()


class AddEmployee(StatesGroup):
    shift_type = State()
    name = State()
    phone_number = State()


@add_employee_router.message(Command("addemployee"))
async def cmd_add_employee(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Дневной",
            callback_data="day"
        ),
        InlineKeyboardButton(
            text="Ночной",
            callback_data="night"
        )
    )

    await message.answer("Укажите тип смены нового сотрудника", reply_markup=builder.as_markup())


@add_employee_router.callback_query(F.data == "day")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(shift_type="Дневной")
    await state.set_state(AddEmployee.name)
    await callback.message.answer("Укажите имя нового сотрудника")


@add_employee_router.callback_query(F.data == "night")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(shift_type="Ночной")
    await state.set_state(AddEmployee.name)
    await callback.message.answer("Укажите имя нового сотрудника")


@add_employee_router.message(AddEmployee.name)
async def add_emloyee_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddEmployee.phone_number)
    await message.answer("Укажите номер телефона нового сотрудника")


@add_employee_router.message(AddEmployee.phone_number)
async def add_emloyee_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    await state.clear()
    db_add_employee(data['shift_type'], data['name'], int(data['phone_number']))
    await message.answer("Новый сотрудник добавлен")
