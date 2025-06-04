from aiogram import Router, types, F
from bot.core.app import cursor
from bot.core.keyboards import get_main_keyboard

router = Router()

@router.message(F.text == "Статистика")
async def show_statistics(message: types.Message):
    user_id = message.from_user.id
    cursor.execute('SELECT SUM(cost) FROM subscriptions WHERE user_id = ?', (user_id,))
    total_cost = cursor.fetchone()[0]

    if total_cost:
        await message.answer(f"Текущая сумма расходов на подписки: {total_cost} руб.",
                            reply_markup=get_main_keyboard())
    else:
        await message.answer("У вас нет активных подписок", reply_markup=get_main_keyboard())