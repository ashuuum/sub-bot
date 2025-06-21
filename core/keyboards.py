from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# ----- Основная клавиатура бота -----
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            #  Первый ряд кнопок
            [KeyboardButton(text="Мои подписки"), KeyboardButton(text="Добавить подписку")],
            #  Второй ряд кнопок
            [KeyboardButton(text="Удалить подписку"), KeyboardButton(text="Редактировать подписку")],
        ],
        resize_keyboard=True  # автоматически подстроить размер клавиатуры под экран телефона
    )