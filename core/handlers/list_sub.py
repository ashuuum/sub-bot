import logging  # логирование
from aiogram import Router, types, F
from datetime import datetime  # преобразование даты
from core.keyboards import get_main_keyboard  # основная клавиатура
from core.app import get_subscriptions_db  # работа с БД


router = Router()  # создание объекта роутера — в него будут добавляться хендлеры
logger = logging.getLogger(__name__) # получение логгера для текущего модуля


# --- Хендлер: пользователь нажал кнопку "Мои подписки" ---

@router.message(F.text == "Мои подписки")
async def list_subscriptions(message: types.Message):
    logger.info(f"Пользователь {message.from_user.id} выполнил запрос на получения списка подписок")  # логирование
    user_id = message.from_user.id  # получение ID пользователя из сообщения

    subscriptions = get_subscriptions_db(user_id)  # получение списка подписок пользователя

    if subscriptions:
        # Сортировка подписок по дате окончания
        subscriptions.sort(key=lambda x: datetime.strptime(x[2], '%Y-%m-%d'))

        # Формирование текст ответа
        response = ""
        for name, cost, end_date in subscriptions:
            # Преобразуем дату в формат ДД.ММ.ГГГГ
            formatted_end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d.%m.%Y')
            response += (
                f"✅ <b>{name}</b>\n"
                f"Стоимость: {int(cost)} руб.\n"
                f"Действует до: {formatted_end_date}\n\n"
            )
    else:
        response = "У вас нет активных подписок"

    # Отправляем ответ пользователю
    await message.answer(response, reply_markup=get_main_keyboard(), parse_mode='HTML')
