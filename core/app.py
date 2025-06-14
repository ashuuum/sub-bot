import aiosqlite
import os
from dotenv import load_dotenv


# --- Конфигурация ---
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
DB_PATH = "core/sub.db"


# --- Инициализация базы: вызывается один раз при старте приложения ---
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            cost INTEGER NOT NULL,
            end_date TEXT NOT NULL
        )
        ''')
        await db.commit()


# --- Добавление новой подписки ---
async def add_subscription_db(user_id, name, cost, end_date):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO subscriptions (user_id, name, cost, end_date) VALUES (?, ?, ?, ?)",
            (user_id, name, cost, end_date))
        await db.commit()


# --- Получение подписок пользователя ---
async def get_subscriptions_db(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT name, cost, end_date FROM subscriptions WHERE user_id = ?", (user_id,))
        rows = await cursor.fetchall()
        return rows


# --- Обновление подписки ---
async def update_subscription_db(user_id: int, old_name: str, new_name: str, cost: float, end_date: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('UPDATE subscriptions SET name = ?, cost = ?, end_date = ? WHERE user_id = ? AND name = ?',
                         (new_name, cost, end_date, user_id, old_name))
        await db.commit()




# --- Удаление подписки ---
async def del_subscription_db(user_id, name):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM subscriptions WHERE user_id = ? AND name = ?", (user_id, name))
        await db.commit()


# --- Получение подписок с истекающим сроком ---
async def get_expiring_subscriptions(date: str):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT user_id, name FROM subscriptions WHERE end_date = ?", (date,))
        rows = await cursor.fetchall()
        return rows