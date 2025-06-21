from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from core.app import get_subscriptions_db, update_subscription_db
from core.keyboards import get_main_keyboard


router = Router()

# Временное хранилище редактируемых подписок: user_id -> old_name
edit_sessions: dict[int, str] = {}


# --- Хендлер: пользователь нажал кнопку "Редактировать подписку" ---
@router.message(F.text == "Редактировать подписку")
async def edit_subscription(message: Message):
    user_id = message.from_user.id
    subscriptions = await get_subscriptions_db(user_id)

    if subscriptions:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=sub[0], callback_data=f"edit_{sub[0]}")] for sub in subscriptions
        ])
        await message.answer("Выберите подписку для редактирования:", reply_markup=keyboard)
    else:
        await message.answer("У вас нет активных подписок", reply_markup=get_main_keyboard())


# --- Хендлер: пользователь нажал на конкретную подписку ---
@router.callback_query(F.data.startswith("edit_"))
async def process_edit_subscription(call: CallbackQuery):
    user_id = call.from_user.id
    old_name = call.data.replace("edit_", "")
    edit_sessions[user_id] = old_name  # сохранить выбранную подписку

    await call.message.answer(
        f"Введите новые данные для подписки '{old_name}' в формате:\n\n"
        f"`имя, стоимость, дата окончания (ДД.ММ.ГГГГ)`",
        parse_mode="Markdown"
    )


# --- Хендлер: пользователь ввёл новые данные (если активна сессия редактирования) ---
@router.message()
async def handle_edit_data(message: Message):
    user_id = message.from_user.id

    if user_id not in edit_sessions:
        return  # нет активной сессии — игнорируем

    old_name = edit_sessions.pop(user_id)

    try:
        name, cost, end_date = map(str.strip, message.text.split(","))
        cost = int(cost)
        end_date_fmt = datetime.strptime(end_date, "%d.%m.%Y").strftime("%Y-%m-%d")

        await update_subscription_db(user_id, old_name, name, cost, end_date_fmt)

        await message.answer(
            f"✅ Подписка успешно обновлена:\n"
            f"📌 *{name}*\n💸 {cost} руб.\n📅 до {end_date}",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        print(f"[ERROR] Ошибка при обновлении подписки: {e}")
        await message.answer("❌ Ошибка. Проверьте формат ввода: имя, стоимость, дата (ДД.ММ.ГГГГ)")
