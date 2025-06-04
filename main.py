import asyncio # для запуска асинхронного цикла
import logging # для ведения логов
from aiogram import Bot, Dispatcher # импорт класса бота и диспетчера
from bot.core.app import API_TOKEN
from bot.core.check_sub import scheduler # импорт токена и планировщика
from bot.handlers import router # импорт роутера с обработчиками


# --- Настройка логирования ---

logging.basicConfig(
    level=logging.INFO,  # задает уровень логирования - INFO и выше (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # задает формат сообщений
    handlers=[
        logging.FileHandler("bot/log/bot.log"),  # запись логов в файл
        logging.StreamHandler()  # вывод логов в консоль
    ]
)
logger = logging.getLogger(__name__) # получение логина для текущего модуля main.py


async def main():
    logger.info("Starting bot...") # логирование запуска бота

    bot = Bot(token=API_TOKEN) # создание объекта бота, передав в него TOKEN
    dp = Dispatcher() # создание диспетчера для регистрации и обработки событий
    dp.include_router(router) # подключение роутера с обработчиками

    scheduler.start() # запуск планировщика
    logger.info("Scheduler started.") # логирование запуска планировщика

    await dp.start_polling(bot) # запуск бота в режиме long polling


if __name__ == "__main__":
    try:
        asyncio.run(main()) # запуск функции main в асинхронном цикле
    except Exception as e:
        logger.critical(f"Bot stopped with error: {e}") # логирование в случае ошибки
