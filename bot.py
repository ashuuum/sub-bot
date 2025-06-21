import asyncio  # для запуска асинхронного цикла
from aiogram import Bot, Dispatcher  # импорт класса бота и диспетчера
from core.app import API_TOKEN, init_db
from core.check_sub import scheduler
from core.handlers import router


async def main():
    await init_db()

    bot = Bot(token=API_TOKEN)  # создание объекта бота, передав в него TOKEN
    dp = Dispatcher()  # создание диспетчера для регистрации и обработки событий
    dp.include_router(router)  # подключение роутера с обработчиками
    scheduler.start()  # запуск планировщика

    await dp.start_polling(bot)  # запуск бота в режиме long polling


if __name__ == "__main__":
    asyncio.run(main())  # запуск функции main в асинхронном цикле
