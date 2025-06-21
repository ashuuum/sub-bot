from aiogram import Router, F, types  # импорт основных компонентов aiogram
from aiogram.fsm.state import StatesGroup, State  # импорт классов для состояний FSM
from aiogram.fsm.context import FSMContext  # импорт контекста FSM
from datetime import datetime  # обработка даты
from core.app import add_subscription_db  # работа с БД
from core.keyboards import get_main_keyboard  # основная клавиатура


router = Router()  # создание роутера — в него будут добавляться хендлеры


# --- Состояния FSM для добавления подписки ---
class AddSubState(StatesGroup):
    waiting_for_sub_data = State()  # ожидание ввода данных пользователем


# --- Хендлер: пользователь нажал кнопку "Добавить подписку" ---
@router.message(F.text == "Добавить подписку")
async def add_subscription(message: types.Message, state: FSMContext):
    await message.answer("Введите через запятую название подписки, стоимость, дату окончания (ДД.ММ.ГГГГ)")
    await state.set_state(AddSubState.waiting_for_sub_data)  # установка состояния ожидания ввода


# --- Хендлер: пользователь ввёл данные подписки ---
@router.message(AddSubState.waiting_for_sub_data)
async def process_subscription(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  # получение ID пользователя из сообщения
    try:
        name, cost, end_date = map(str.strip, message.text.split(','))  # разбиение ввода пользователя
        cost = int(cost)

        end_date = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")  # конвертирование формата даты

        await add_subscription_db(user_id, name, cost, end_date)  # добавление новой подписки в базу данных

        # Вывод пользователю сообщения и клавиатуры
        await message.answer(f"Подписка '{name}' добавлена!", reply_markup=get_main_keyboard())
        await state.clear()  # сброс состояния FSM
    except ValueError:
        await message.reply("Ошибка в формате данных. Убедитесь, что вы используете: имя, стоимость, дата (ДД.ММ.ГГГГ)")
        await state.clear()  # сброс состояния FSM