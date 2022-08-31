import config

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
