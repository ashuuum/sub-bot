from aiogram import Router, types, F
from core.keyboards import get_main_keyboard  # для получения основной клавиатуры
import logging

router = Router()
logger = logging.getLogger(__name__)


# --- Хендлер: пользователь ввел "/start" для запуска бота ---

@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} запустил бота")  # логирование запуска

    await message.reply(
        "Привет! Я бот для отслеживания подписок. Выбери действие:",
        reply_markup=get_main_keyboard()  # вывод клавиатуры на экран
    )