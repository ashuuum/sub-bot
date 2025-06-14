import logging  # логирование
from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from core.keyboards import get_main_keyboard  # для получения основной клавиатуры
from core.app import get_subscriptions_db, del_subscription_db  # работа с БД


router = Router()  # создание роутера — в него будут добавляться хендлеры
logger = logging.getLogger(__name__)  # получение логгера для текущего модуля


# --- Хендлер: пользователь нажал кнопку "Удалить подписку" ---

@router.message(F.text == "Удалить подписку")
async def edit_subscription(message: Message):
    user_id = message.from_user.id  # получение ID пользователя из сообщения

    subscriptions = get_subscriptions_db(user_id)  # получение подписок пользователя

    if subscriptions:
        # Создание inline-клавиатуры с кнопками по одной на каждую подписку
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"delete_{name}")] for (name,) in subscriptions
        ])
        # Вывод пользователю сообщения и клавиатуры
        await message.reply("Выберите подписку для редактирования:", reply_markup=keyboard)
    else:
        await message.reply("У вас нет активных подписок", reply_markup=get_main_keyboard())


# --- Хендлер: пользователь нажал кнопку с конкретной подпиской ---

@router.callback_query(F.data.startswith("delete_"))
async def process_delete_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id
    name = call.data.replace("delete_", "")
    await del_subscription_db(user_id, name)  # удаление подписки
    logger.info(f"Пользователь {user_id} добавил новую подписку: {name}")  # логирование
    await call.message.answer(f"Подписка '{name}' удалена.", reply_markup=get_main_keyboard())