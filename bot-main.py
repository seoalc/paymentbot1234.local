from aiogram.utils import executor
from bot_create import dp
import asyncio
from handlers import mainhand

async def on_startup(_):
    print('Бот вышел в онлайн')

mainhand.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
