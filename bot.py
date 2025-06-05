import asyncio # для запуска асинхронного цикла
import logging # для ведения логов
from aiogram import Bot, Dispatcher # импорт класса бота и диспетчера
from core.app import API_TOKEN
from core.check_sub import scheduler # импорт токена и планировщика
from core.handlers import router # импорт роутера с обработчиками


# --- Настройка логирования ---

logging.basicConfig(
    level=logging.INFO,  # задает уровень логирования - INFO и выше (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # задает формат сообщений
    handlers=[
        logging.FileHandler("core/file.log"),  # запись логов в файл
        logging.StreamHandler()  # вывод логов в консоль
    ]
)
logger = logging.getLogger(__name__) # получение логина для текущего модуля core.py


async def main():
    logger.info("Запуск бота") # логирование запуска бота

    bot = Bot(token=API_TOKEN) # создание объекта бота, передав в него TOKEN
    dp = Dispatcher() # создание диспетчера для регистрации и обработки событий
    dp.include_router(router) # подключение роутера с обработчиками

    scheduler.start() # запуск планировщика
    logger.info("Запуск планировщика") # логирование запуска планировщика

    await dp.start_polling(bot) # запуск бота в режиме long polling


if __name__ == "__main__":
    try:
        asyncio.run(main()) # запуск функции main в асинхронном цикле
    except Exception as e:
        logger.critical(f"Бот остановлен из за ошибки: {e}") # логирование в случае ошибки
