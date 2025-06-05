from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime # для преобразования даты
from core.app import get_user_subscriptions, update_subscription, parse_date  # для работы с БД и датами
from core.keyboards import get_main_keyboard # для получения основной клавиатуры


router = Router() # создание объекта роутера — в него будут добавляться хендлеры


# --- Состояние для редактирования подписки ---

class EditSubscriptionState(StatesGroup):
    waiting_for_new_data = State()  # ожидание ввода данных


# --- Хендлер: пользователь нажал кнопку "Редактировать подписку" ---

@router.message(F.text == "Редактировать подписку")
async def edit_subscription(message: Message):
    user_id = message.from_user.id  # получение ID пользователя из сообщения

    subscriptions = get_user_subscriptions(user_id)  # получение подписок пользователя

    if subscriptions:
        # Создание inline-клавиатуры с кнопками по одной на каждую подписку
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"edit_{name}")] for (name,) in subscriptions
        ])
        # Вывод пользователю сообщения и клавиатуры
        await message.reply("Выберите подписку для редактирования:", reply_markup=keyboard)
    else:
        # Вывод сообщения в случае отсутствуя подписок и отображение начальной клавиатуры
        await message.reply("У вас нет активных подписок.", reply_markup=get_main_keyboard())


# --- Хендлер: пользователь нажал кнопку с конкретной подпиской ---

@router.callback_query(F.data.startswith("edit_"))
async def process_edit_subscription(call: CallbackQuery, state: FSMContext):
    old_name = call.data.replace("edit_", "")  # получение названия подписки
    await state.update_data(old_name=old_name)  # сохранение название во временное состояние

    # Вывод просьбы указать новые данные
    await call.message.answer(
        f"Введите новые данные для '{old_name}' в формате: имя, стоимость, дата окончания (ДД.ММ.ГГГГ)")
    await state.set_state(EditSubscriptionState.waiting_for_new_data)  # устанавливается состояние ожидания ввода


# --- Хендлер: пользователь ввёл новые данные для подписки ---

@router.message(EditSubscriptionState.waiting_for_new_data)
async def process_edit_data(message: Message, state: FSMContext):
    user_id = message.from_user.id  # получение ID пользователя из сообщения
    data = await state.get_data()  # получение временного состояния (названия подписки)
    old_name = data.get("old_name")

    try:
        name, cost, end_date = map(str.strip, message.text.split(','))  # разбиение ввода пользователя
        cost = int(cost)
        end_date = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")  # конвертирование формата даты

        # Обновление подписки в базе данных
        update_subscription(user_id, old_name, name, cost, end_date)

        # Вывод сообщения об успешном обновлении подписки
        await message.answer(f"Подписка '{name}' обновлена!\nНовая стоимость: {cost} руб."
                             f"\nДата окончания: {end_date}.", reply_markup=get_main_keyboard())
        await state.clear()  # сброс состояния FSM
    except ValueError:
        # Вывод сообщения об ошибки
        await message.reply("Ошибка в формате данных. Убедитесь, что вы используете: имя, стоимость, дата (ДД.ММ.ГГГГ)")