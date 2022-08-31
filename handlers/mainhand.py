from aiogram import types, Dispatcher
from bot_create import dp, bot, p2p
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from db import dbusers
from keyboards import paymentAmount_kb
from pyqiwip2p import QiwiP2P

# @dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
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
        await message.reply(forUserTxt, reply_markup=paymentAmount_kb)
    except:
        await message.reply('Возникла какая-то ошибка, попробуйте повторить команду /start')

# новый стейт и загрузка сообщения от пользователя с суммой платежа
class FSMNewpayamount(StatesGroup):
    payamount = State()

@dp.callback_query_handler(text='getPaymentAmount')
async def send_payment_amount(callback : types.CallbackQuery):
    tg_id = callback.from_user.id
    await FSMNewpayamount.payamount.set()
    await bot.send_message(callback.from_user.id, 'Введите сумму платежа цифрами')
    await callback.answer()

# ответ пользователя пишется в словать
# @dp.message_handler(state=FSMNewpayamount.payamount)
async def get_payment_amount(message: types.Message, state: FSMContext):
    paymentMount = message.text
    if paymentMount.isdigit() == True:
        if paymentMount >= 1:
            async with state.proxy() as data:
                data['payamount'] = message.text
            # applId = await dbusers.addNewApplicant(state)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, 'Минимальная сумма пополнения 1 руб.')
    else:
        await bot.send_message(message.from_user.id, 'Введите целое число')




def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(get_payment_amount, state=FSMNewpayamount.payamount)
