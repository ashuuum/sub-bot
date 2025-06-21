from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from core.keyboards import get_main_keyboard
from core.app import get_subscriptions_db, del_subscription_db


router = Router()  # создание роутера — в него будут добавляться хендлеры


# --- Хендлер: пользователь нажал кнопку "Удалить подписку" ---
@router.message(F.text == "Удалить подписку")
async def edit_subscription(message: Message):
    user_id = message.from_user.id  # получение ID пользователя из сообщения

    subscriptions = await get_subscriptions_db(user_id)  # получение подписок пользователя

    if subscriptions:
        # Создание inline-клавиатуры с кнопками по одной на каждую подписку
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=sub[0],
                                  callback_data=f"delete_{sub[0]}")] for sub in subscriptions])
        # Вывод пользователю сообщения и клавиатуры
        await message.answer("Выберите подписку для удаления:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет активных подписок", reply_markup=get_main_keyboard())


# --- Хендлер: пользователь нажал кнопку с конкретной подпиской ---
@router.callback_query(F.data.startswith("delete_"))
async def process_delete_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id
    name = call.data.replace("delete_", "")
    await del_subscription_db(user_id, name)  # удаление подписки
    await call.message.answer(f"Подписка '{name}' удалена.", reply_markup=get_main_keyboard())