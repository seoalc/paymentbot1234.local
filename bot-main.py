from aiogram.utils import executor
from bot_create import dp
import asyncio
from handlers import mainhand, adminhand
import logging

# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='warnings.log', level=logging.WARNING,
#                     format='%(asctime)s')
# logging.basicConfig(filename='errors.log', level=logging.ERROR)

async def on_startup(_):
    print('Бот вышел в онлайн')

mainhand.register_handlers_client(dp)
adminhand.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
