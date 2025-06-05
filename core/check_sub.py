import logging
from aiogram import Bot
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # работа с планировщиком задач

from core.app import API_TOKEN
from core.app import get_expiring_subscriptions


# --- Загрузка конфигурации ---

logger = logging.getLogger(__name__)  # загрузка переменной окружения из файла .env
bot = Bot(token=API_TOKEN)  # чтение переменной окружения API_TOKEN


async def check_subscriptions():
    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"Проверка подписок на сегодня: {today}") # логирование

    subscriptions = get_expiring_subscriptions(today)

    if subscriptions:
        for user_id, name in subscriptions:
            logger.info(f"Отправлено напоминание пользователю {user_id} об окончании подписки '{name}'") # логирование
            await bot.send_message(user_id, f"❗️Напоминание: подписка '{name}' заканчивается сегодня!")
    else:
        logger.info("На сегодня нет оканчивающихся подписок") # логирование


# ----- Планировщик -----

scheduler = AsyncIOScheduler() # создание экземпляра планировщика, работающего с асинхронным циклом
scheduler.add_job(check_subscriptions, 'interval', days=1) # добавление задачи "проверка подписки"