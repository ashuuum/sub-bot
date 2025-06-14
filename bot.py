import asyncio  # для запуска асинхронного цикла
import logging  # для ведения логов
from aiogram import Bot, Dispatcher  # импорт класса бота и диспетчера
from core.app import API_TOKEN, init_db
from core.check_sub import scheduler  # импорт токена и планировщика
from core.handlers import router  # импорт роутера с обработчиками


LOG_PATH = "core/file.log"


# --- Настройка логирования ---
logging.basicConfig(
    level=logging.INFO,  # задает уровень логирования - INFO и выше (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # задает формат сообщений
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()]  # запись логов в файо и вывод в консоль
)
logger = logging.getLogger(__name__)  # получение логера для текущего модуля


async def main():
    logger.info("Запуск бота")

    await init_db()

    bot = Bot(token=API_TOKEN)  # создание объекта бота, передав в него TOKEN
    dp = Dispatcher()  # создание диспетчера для регистрации и обработки событий
    dp.include_router(router)  # подключение роутера с обработчиками

    scheduler.start()  # запуск планировщика
    logger.info("Запуск планировщика")

    await dp.start_polling(bot)  # запуск бота в режиме long polling


if __name__ == "__main__":
    try:
        asyncio.run(main())  # запуск функции main в асинхронном цикле
    except Exception as e:
        logger.critical(f"Бот остановлен из за ошибки: {e}")
