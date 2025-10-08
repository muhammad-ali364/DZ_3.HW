import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import ClientTimeout

# -------------------------------
# Загружаем переменные окружения
# -------------------------------
load_dotenv()
TOKEN = os.getenv("TOKEN")  # обязательно в .env должно быть TOKEN
ADMIN_ID = int(os.getenv("ADMIN_ID", "5199401134"))

# -------------------------------
# Настройка логирования
# -------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------
# Создаем объект бота с таймаутом
# -------------------------------
timeout = ClientTimeout(total=60)
bot = Bot(token=TOKEN, timeout=timeout)
dp = Dispatcher()

# -------------------------------
# Команда /start
# -------------------------------
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Бот готов принимать уведомления!")

# -------------------------------
# Функция отправки уведомлений
# -------------------------------
async def send_car_notification(car_data: dict):
    """
    Асинхронная отправка уведомления о новой машине.
    car_data: dict с ключами user, brand, model, number, date, carabka_transfer, type_car, probeg
    """
    text = (
        f"🚗 Новый автомобиль добавлен!\n\n"
        f"👤 Владелец: {car_data.get('user', 'Аноним')}\n"
        f"🏷️ Бренд: {car_data.get('brand')}\n"
        f"🚘 Модель: {car_data.get('model')}\n"
        f"🔢 Номер: {car_data.get('number')}\n"
        f"📅 Дата: {car_data.get('date')}\n"
        f"⚙️ КПП: {car_data.get('carabka_transfer')}\n"
        f"🚗 Тип: {car_data.get('type_car')}\n"
        f"📍 Пробег: {car_data.get('probeg')}\n"
    )
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=text)
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления: {e}")

# -------------------------------
# Функция для вызова из Django
# -------------------------------
def send_notification_sync(car_data: dict):
    """
    Синхронная обёртка для вызова из Django.
    Создает свой loop, чтобы избежать ошибки Event loop is closed.
    """
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_car_notification(car_data))
    except Exception as e:
        logger.error(f"Ошибка при синхронной отправке уведомления: {e}")
    finally:
        loop.close()

# -------------------------------
# Основная функция запуска бота
# -------------------------------
async def main():
    print("✅ Бот запущен и готов к работе")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# -------------------------------
# Запуск бота напрямую (для разработки)
# -------------------------------
if __name__ == "__main__":
    asyncio.run(main())
