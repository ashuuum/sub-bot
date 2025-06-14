import os
import sqlite3
from dotenv import load_dotenv  # работа с .env


# --- Загрузка конфигурации ---

load_dotenv()  # загрузка переменной окружения из файла .env
API_TOKEN = os.getenv("API_TOKEN")  # чтение переменной окружения API_TOKEN


# --- Работа с базой данных ---

conn = sqlite3.connect("core/sub.db", check_same_thread=False) # подключение к базе данных SQLite
cursor = conn.cursor() # получение курсора для выполнения SQL-запроса

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    cost INTEGER NOT NULL,
    end_date TEXT NOT NULL
)
''')
conn.commit()


# Функция добавляет новую подписку
def add_subscription_db(user_id, name, cost, end_date):
    cursor.execute(
        '''INSERT INTO subscriptions (user_id, name, cost, end_date) VALUES (?, ?, ?, ?)''',
        (user_id, name, cost, end_date)
    )
    conn.commit()


# Функция возвращает список подписок пользователя
def get_subscriptions_db(user_id: int):
    cursor.execute('SELECT name FROM subscriptions WHERE user_id = ?', (user_id,))
    return cursor.fetchall()


# Функция изменяет подписку пользователя
def update_subscription_db(user_id: int, old_name: str, new_name: str, cost: float, end_date: str):
    cursor.execute('UPDATE subscriptions SET name = ?, cost = ?, end_date = ? WHERE user_id = ? AND name = ?',
        (new_name, cost, end_date, user_id, old_name)
    )
    conn.commit()


# Функция удаляет подписку
def del_subscription_db(user_id, name):
    cursor.execute('DELETE FROM subscriptions WHERE user_id = ? AND name = ?',
                   (user_id, name)
    )
    conn.commit()


# Возвращает список подписок, срок действия которых истекает в заданную дату
def get_expiring_subscriptions(date: str):
    cursor.execute('SELECT user_id, name FROM subscriptions WHERE end_date = ?', (date,))
    return cursor.fetchall()