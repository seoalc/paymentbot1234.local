import config

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from pyqiwip2p import QiwiP2P

storage = MemoryStorage()

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
# qiwi api init
p2p = QiwiP2P(auth_key=config.QIWI_TOKEN)
