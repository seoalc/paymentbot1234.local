from aiogram import types, Dispatcher
from bot_create import dp, bot, p2p
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from db import dbusers, dbpayments, dbadmins
from keyboards import mainAdmin_kb, sendLogs_kb

# @dp.message_handler(commands=['admin'])
async def command_admin(message : types.Message):
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
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Вас нет в списке администраторов бота'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            adminMainText = 'Вы в главном меню администратора'
            await message.reply(adminMainText, reply_markup=mainAdmin_kb)
    except:
        await message.reply('Возникла какая-то ошибка, попробуйте повторить команду /start')

# @dp.message_handler(commands=['посмотреть пользователей'])
async def show_users(message : types.Message):
    try:
        tg_id = message.from_user.id
        tg_name = message.from_user.first_name
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            adminMainText = 'Список пользователей'
            await message.reply(adminMainText)
            allUsers = dbusers.getAllUsers()
            for item in allUsers:
                eachUserText = '<b>Телеграм id:</b>\n' + str(item['tg_id']) + '\n'\
                                '<b>Текущий баланс:</b>\n' + str(item['user_check']) + '\n'
                if item['blocked'] == 0:
                    calText = 'Заблокировать пользователя'
                    calCommand = 'blockUser_'
                else:
                    calText = 'Разблокировать пользователя'
                    calCommand = 'unblockUser_'
                button = InlineKeyboardMarkup(row_width=1)
                button.add(InlineKeyboardButton(text='Изменить баланс',
                                                callback_data='editBalanceUser_' + str(item['tg_id']))).\
                        add(InlineKeyboardButton(text=calText,
                                                        callback_data=calCommand + str(item['tg_id'])))
                await message.answer(eachUserText, parse_mode=types.ParseMode.HTML, reply_markup=button)
    except:
        await message.reply('Возникла какая-то ошибка, попробуйте повторить команду /start')

class FSMEditusersbalance(StatesGroup):
    edituserbal = State()
# действия по нажатию инлайн кнопки изменить баланс пользователя
@dp.callback_query_handler(Text(startswith='editBalanceUser_'))
async def edit_balance_user(callback : types.CallbackQuery):
    try:
        tg_id = callback.from_user.id
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            userTGId = callback.data.split('_')[1]
            usBal = dbusers.getUsersCheckByTgId(userTGId)
            await FSMEditusersbalance.edituserbal.set()
            await bot.send_message(callback.from_user.id, 'Текущий баланс пользователя - ' + str(usBal['user_check']) + \
                                                '\n\nВведите новое значение')
    except:
        await bot.send_message(callback.from_user.id, 'Возникла какая-то ошибка, попробуйте повторить команду /start')
        await callback.answer()

# Продолжение машинного состояния по ловле изменяемого баланса пользователя
# @dp.message_handler(state=FSMEditusersbalance.edituserbal)
async def get_new_balance_user(callback : types.CallbackQuery, state: FSMEditusersbalance):
    async with state.proxy() as data:
        data['newBal'] = callback.text
        data['tg_id'] = callback.from_user.id
        await dbusers.updtUsersBalance(data['newBal'], data['tg_id'])
        await state.finish()
        await bot.send_message(callback.from_user.id, 'Баланс пользователя изменен на '+callback.text, reply_markup=mainAdmin_kb)

# действия по нажатию инлайн кнопки изменить заблокировать пользователя
@dp.callback_query_handler(Text(startswith='blockUser_'))
async def block_user(callback : types.CallbackQuery):
    try:
        tg_id = callback.from_user.id
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            userTGId = callback.data.split('_')[1]
            await dbusers.blockUserByTgId(userTGId)
            await bot.send_message(callback.from_user.id, 'Пользователь '+userTGId+' заблокирован', reply_markup=mainAdmin_kb)
    except:
        await bot.send_message(callback.from_user.id, 'Возникла какая-то ошибка, попробуйте повторить команду /start')
        await callback.answer()

# действия по нажатию инлайн кнопки изменить разблокировать пользователя
@dp.callback_query_handler(Text(startswith='unblockUser_'))
async def block_user(callback : types.CallbackQuery):
    try:
        tg_id = callback.from_user.id
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            userTGId = callback.data.split('_')[1]
            await dbusers.unblockUserByTgId(userTGId)
            await bot.send_message(callback.from_user.id, 'Пользователь '+userTGId+' разблокирован', reply_markup=mainAdmin_kb)
    except:
        await bot.send_message(callback.from_user.id, 'Возникла какая-то ошибка, попробуйте повторить команду /start')
        await callback.answer()

# @dp.message_handler(commands=['выгрузить логи'])
async def get_logs(message : types.Message):
    try:
        tg_id = message.from_user.id
        tg_name = message.from_user.first_name
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            adminMainText = 'Какой тип логов выгрузить?'
            await message.answer(adminMainText, reply_markup=sendLogs_kb)
    except:
        await message.reply('Возникла какая-то ошибка, попробуйте повторить команду /start')

# @dp.message_handler(commands=['предупреждения warning'])
async def send_war_log_file(message : types.Message):
    try:
        tg_id = message.from_user.id
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            await message.reply_document(open('warnings.log', 'rb'), reply_markup=mainAdmin_kb)
    except:
        await bot.send_message(callback.from_user.id, 'Возникла какая-то ошибка, попробуйте повторить команду /start')
        await callback.answer()

# @dp.message_handler(commands=['ошибки error'])
async def send_err_log_file(message : types.Message):
    try:
        tg_id = message.from_user.id
        countUser = dbusers.checkUserByTgId(tg_id)
        if countUser == 0:
            dbusers.addNewUser(tg_id)
        elif countUser == 1:
            usersCheck = dbusers.getUsersCheckByTgId(tg_id)
        countAdmin = dbadmins.checkAdminByTgId(tg_id)
        if countAdmin == 0:
            accesDeniedAdmTxt = 'Данная команда вам недоступна'
            await message.reply(accesDeniedAdmTxt)
        elif countAdmin == 1:
            await message.reply_document(open('errors.log', 'rb'), reply_markup=mainAdmin_kb)
    except:
        await bot.send_message(callback.from_user.id, 'Возникла какая-то ошибка, попробуйте повторить команду /start')
        await callback.answer()


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_admin, commands=['admin'])
    dp.register_message_handler(show_users, Text(equals="посмотреть пользователей", ignore_case=True))
    dp.register_message_handler(get_new_balance_user, state=FSMEditusersbalance.edituserbal)
    dp.register_message_handler(get_logs, Text(equals="выгрузить логи", ignore_case=True))
    dp.register_message_handler(send_war_log_file, Text(equals="предупреждения warning", ignore_case=True))
    dp.register_message_handler(send_err_log_file, Text(equals="ошибки error", ignore_case=True))
