from aiogram import types, Dispatcher
from bot_create import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        tg_id = message.from_user.id
        await message.reply('saluteText')
    except:
        await message.reply('Возникла какая-то ошибка, попробуйте повторить команду /start')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
