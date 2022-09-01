from aiogram import types, Dispatcher
from bot_create import dp, bot, p2p
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from db import dbusers, dbpayments, dbadmins

# @dp.message_handler(commands=['admin'])
async def command_admin(message : types.Message):
    # try:
    #     tg_id = message.from_user.id
    #     tg_name = message.from_user.first_name
    #     countUser = dbusers.checkUserByTgId(tg_id)
    #     if countUser == 0:
    #         dbusers.addNewUser(tg_id)
    #         forUserTxt = 'Привет, ' + tg_name + '\nЯ - бот для пополнения баланса.\nНажмите на кнопку, чтобы пополнить баланс\n'\
    #                         'Ваш текущий баланс 0'
    #     elif countUser == 1:
    #         usersCheck = dbusers.getUsersCheckByTgId(tg_id)
    #         forUserTxt = 'Привет, ' + tg_name + '\nЯ - бот для пополнения баланса.\nНажмите на кнопку, чтобы пополнить баланс\n'\
    #                         'Ваш текущий баланс ' + str(usersCheck['user_check'])
    #     countAdmin = dbadmins.checkAdminByTgId(tg_id)
    #     print (countAdmin)
    #     await message.reply(forUserTxt, reply_markup=paymentAmount_kb)
    # except:
    #     await message.reply('Возникла какая-то ошибка, попробуйте повторить команду /start')
    tg_id = message.from_user.id
    tg_name = message.from_user.first_name
    countUser = dbusers.checkUserByTgId(tg_id)
    if countUser == 0:
        dbusers.addNewUser(tg_id)
        forUserTxt = 'Привет, ' + tg_name + '\nЯ - бот для пополнения баланса.\nНажмите на кнопку, чтобы пополнить баланс\n'\
                        'Ваш текущий баланс 0'
    elif countUser == 1:
        usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        forUserTxt = 'Привет, ' + tg_name + '\nЯ - бот для пополнения баланса.\nНажмите на кнопку, чтобы пополнить баланс\n'\
                        'Ваш текущий баланс ' + str(usersCheck['user_check'])
    countAdmin = dbadmins.checkAdminByTgId(tg_id)
    if countAdmin == 0:
        accesDeniedAdmTxt = 'Вас нет в списке администраторов бота'
        await message.reply(accesDeniedAdmTxt)
    elif countAdmin == 1:
        pass
    # await message.reply(forUserTxt, reply_markup=paymentAmount_kb)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_admin, commands=['admin'])
