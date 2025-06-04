from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.core.app import cursor, conn
from bot.core.keyboards import get_main_keyboard

router = Router()

@router.message(F.text == "Удалить подписку")
async def remove_subscription(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT name FROM subscriptions WHERE user_id = ?', (user_id,))
    subscriptions = cursor.fetchall()

    if subscriptions:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=name, callback_data=f"delete_{name}")] for (name,) in subscriptions
        ])
        await message.answer("Выберите подписку для удаления:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет активных подписок.", reply_markup=get_main_keyboard())

@router.callback_query(F.data.startswith("delete_"))
async def process_delete_subscription(call: types.CallbackQuery):
    user_id = call.from_user.id
    name = call.data.replace("delete_", "")
    cursor.execute('DELETE FROM subscriptions WHERE user_id = ? AND name = ?', (user_id, name))
    conn.commit()
    await call.message.answer(f"Подписка '{name}' удалена.", reply_markup=get_main_keyboard())