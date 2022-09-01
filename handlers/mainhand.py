from aiogram import types, Dispatcher
from bot_create import dp, bot, p2p
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from db import dbusers, dbpayments
from keyboards import paymentAmount_kb
from pyqiwip2p import QiwiP2P
import random

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
    await FSMNewpayamount.payamount.set()
    await bot.send_message(callback.from_user.id, 'Введите сумму платежа цифрами')
    await callback.answer()

# ответ пользователя пишется в словать
# @dp.message_handler(state=FSMNewpayamount.payamount)
async def get_payment_amount(message: types.Message, state: FSMContext):
    # генерация случайного id
    randId = message.from_user.id + int(''.join([random.choice(list('123456789')) for x in range(12)]))
    paymentMount = message.text
    if paymentMount.isdigit() == True:
        if int(paymentMount) >= 1:
            async with state.proxy() as data:
                data['tg_id'] = message.from_user.id
                data['payamount'] = message.text
                # Выставим счет на сумму, введенную пользователем, который будет работать 5 минут
                new_bill = p2p.bill(bill_id=randId, amount=paymentMount, lifetime=5)
                data['new_bill'] = new_bill.bill_id
            await dbpayments.addNewPayment(state)
            # applId = await dbusers.addNewApplicant(state)
            await state.finish()
            forUserPayText = 'Платеж на сумму ' + str(paymentMount) + ' создан.\nНужно подтвердить его'
            # инлайн кнопки со ссылкой для оплаты и проверкой оплаты
            forUserPayButton = InlineKeyboardMarkup(row_width=1)
            forUserPayButton.\
            add(InlineKeyboardButton(text='Ссылка для оплаты', url=p2p.check(bill_id=randId).pay_url)).\
            add(InlineKeyboardButton(text='Проверить статус платежа', callback_data='checkPay_' + new_bill.bill_id))
            await bot.send_message(message.from_user.id, forUserPayText, reply_markup=forUserPayButton)
        else:
            await bot.send_message(message.from_user.id, 'Минимальная сумма пополнения 1 руб.')
    else:
        await bot.send_message(message.from_user.id, 'Введите целое число')

# проверка платежа по id
@dp.callback_query_handler(Text(startswith='checkPay_'))
async def check_pay(callback : types.CallbackQuery):
    # try:
    #     bill = callback.data.split('_')[1]
    #     if dbpayments.checkPaymentById(bill) == 1:
    #         # Проверим статус выставленного счета через его bill_id
    #         print(await p2p.check(bill_id=bill).status)
    #     else:
    #         await bot.send_message(callback.from_user.id, 'Платеж не найден')
    # except:
    #     await bot.send_message(callback.from_user.id, 'Возникла какая-то ошибка, попробуйте повторить команду /start')
    #     await callback.answer()
    bill = callback.data.split('_')[1]
    if dbpayments.checkPaymentById(bill) == 1:
        # Проверим статус выставленного счета через его bill_id
        if p2p.check(bill_id=bill).status == "PAID":
            usersBalance = dbusers.getUsersCheckByTgId(callback.from_user.id)
            paymentAmount = dbpayments.getPaymentAmountByBillId(bill)
            newBalance = int(usersBalance) + int(paymentAmount)
            dbusers.updtUsersBalance(newBalance, callback.from_user.id)
            await bot.send_message(callback.from_user.id, 'Баланс пополнен')
        elif p2p.check(bill_id=bill).status == "WAITING":
            # инлайн кнопки со ссылкой для оплаты и проверкой оплаты
            forUserPayButton = InlineKeyboardMarkup(row_width=1)
            forUserPayButton.\
            add(InlineKeyboardButton(text='Проверить статус платежа', callback_data='checkPay_' + bill))
            await bot.send_message(callback.from_user.id, 'Ожидает оплаты', reply_markup=forUserPayButton)
        elif p2p.check(bill_id=bill).status == "EXPIRED":
            await bot.send_message(callback.from_user.id, 'Платеж просрочен', reply_markup=paymentAmount_kb)
    else:
        await bot.send_message(callback.from_user.id, 'Платеж не найден')


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(get_payment_amount, state=FSMNewpayamount.payamount)
