import logging  # логирование
from aiogram import Router, types, F
from datetime import datetime  # обработка даты
from core.app import add_subscription_db  # работа с БД
from core.keyboards import get_main_keyboard  # основная клавиатура


router = Router()  # создание роутера — в него будут добавляться хендлеры
logger = logging.getLogger(__name__)  # получение логгера для текущего модуля


# --- Хендлер: пользователь нажал кнопку "Добавить подписку" ---

@router.message(F.text == "Добавить подписку")
async def add_subscription(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} выполнил запрос на добавление подписки")  # логирование
    await message.answer("Введите через запятую название подписки, стоимость, дату окончания (ДД.ММ.ГГГГ)")


# --- Хендлер: пользователь ввёл данные подписки ---

@router.message(lambda message: len(message.text.split(',')) == 3 and message.text.startswith("Добавить "))
async def process_subscription(message: types.Message):
    user_id = message.from_user.id  # получение ID пользователя из сообщения
    try:
        name, cost, end_date = map(str.strip, message.text.split(','))  # разбиение ввода пользователя
        cost = int(cost)

        end_date = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")  # конвертирование формата даты

        await add_subscription_db(user_id, name, cost, end_date)  # добавление новой подписки в базу данных
        logger.info(f"Пользователь {user_id} добавил новую подписку: {name}")  # логирование

        # Вывод пользователю сообщения и клавиатуры
        await message.answer(f"Подписка '{name}' добавлена!", reply_markup=get_main_keyboard())
    except ValueError as e:
        logger.error(f"Пользователь {message.from_user.id} ввел неверные данные. "
                     f"Ошибка: {e}") # логирование ошибки
        await message.reply("Ошибка в формате данных. Убедитесь, что вы используете: имя, стоимость, дата (ДД.ММ.ГГГГ)")