# bot_notify.py
import asyncio
import logging
import os
from aiogram import Bot
from aiohttp import ClientTimeout
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("token")
ADMIN_ID = int(os.getenv("ADMIN_ID", "5199401134"))

logging.basicConfig(level=logging.INFO)
timeout = ClientTimeout(total=60)
bot = Bot(token=TOKEN, timeout=timeout)


def send_car_notification_sync(car_data: dict):
    """
    Синхронная обертка для отправки уведомления.
    Создаёт отдельный event loop для каждого вызова.
    """
    async def _send():
        text = (
            f"🚗 Новый автомобиль добавлен!\n\n"
            f"👤 Владелец: {car_data.get('owner', 'Аноним')}\n"
            f"🏷️ Бренд: {car_data.get('brand')}\n"
            f"🚘 Модель: {car_data.get('model')}\n"
            f"🔢 Номер: {car_data.get('number')}\n"
            f"📅 Дата: {car_data.get('date')}\n"
            f"⚙️ КПП: {car_data.get('carabka_transfer')}\n"
            f"🚗 Тип: {car_data.get('type_car')}\n"
            f"📍 Пробег: {car_data.get('probeg')}\n"
        )
        try:
            await bot.send_message(ADMIN_ID, text)
        except Exception as e:
            logging.error(f"Ошибка при отправке уведомления: {e}")
        finally:
            await bot.session.close()

    # Создаём новый loop для каждой отправки
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_send())
    loop.close()
