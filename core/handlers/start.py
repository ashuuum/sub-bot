from aiogram import Router, types, F
from core.keyboards import get_main_keyboard


router = Router()


# --- Хендлер: пользователь ввел "/start" для запуска бота ---
@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот для отслеживания подписок. Выбери действие:",
        reply_markup=get_main_keyboard()  # вывод клавиатуры на экран
    )