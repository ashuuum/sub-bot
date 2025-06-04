from aiogram import Router, types, F
from bot.core.keyboards import get_main_keyboard
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "/start")
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot.")
    await message.reply(
        "Привет! Я бот для отслеживания подписок. Выбери действие:",
        reply_markup=get_main_keyboard()
    )