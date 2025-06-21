from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from core.app import get_subscriptions_db
from core.keyboards import get_main_keyboard


router = Router()  # создание роутера — в него будут добавляться хендлеры


# --- Генерация клавиатуры с кнопками подписок ---
def get_subscription_keyboard(subscriptions):
    buttons = []  # создание списка для кнопок
    for i, (name, cost, end_date) in enumerate(subscriptions):
        formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d.%m.%Y')  # форматирование даты
        button = InlineKeyboardButton(
            text=f"📦 {name} ({formatted_end_date})",
            callback_data=f"sub:{i}"
        )
        buttons.append([button])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# --- Хендлер: пользователь нажал кнопку "Мои подписки" ---
@router.message(F.text == "Мои подписки")
async def list_subscriptions(message: types.Message):
    user_id = message.from_user.id
    subscriptions = await get_subscriptions_db(user_id)

    if subscriptions:
        subscriptions.sort(key=lambda x: datetime.strptime(x[2], '%Y-%m-%d'))
        text = "📋 <b>Ваши подписки:</b>\n\nВыберите, чтобы узнать подробнее"
        keyboard = get_subscription_keyboard(subscriptions)
    else:
        text = "🚫 Нет активных подписок"
        keyboard = get_main_keyboard()

    await message.answer(text, reply_markup=keyboard, parse_mode='HTML')


# --- Хендлер: обработка нажатий по кнопке подписки ---
@router.callback_query(F.data.startswith("sub:"))
async def show_subscription_details(callback: types.CallbackQuery):
    index = int(callback.data.split(":")[1])
    user_id = callback.from_user.id
    subscriptions = await get_subscriptions_db(user_id)

    if 0 <= index < len(subscriptions):
        name, cost, end_date = subscriptions[index]
        formatted_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d.%m.%Y')
        text = (
            f"📄 <b>{name}</b>\n\n"
            f"Стоимость: <i>{int(cost)} ₽</i>\n"
            f"Действует до: <u>{formatted_date}</u>"
        )
        await callback.message.answer(text, reply_markup=get_main_keyboard(), parse_mode='HTML')

    await callback.answer()  # закрываем "часики"
