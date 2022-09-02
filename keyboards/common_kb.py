from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# клавиатура главного меню админа
showUsers = KeyboardButton('Посмотреть пользователей')
uploadLogs = KeyboardButton('Выгрузить логи')
editUser = KeyboardButton('Редактировать пользователя')
# goToHighMenu = KeyboardButton('Вернуться в главное меню')
mainAdmin_kb = ReplyKeyboardMarkup(resize_keyboard=True)
mainAdmin_kb.add(showUsers).add(uploadLogs).add(editUser)

# клавиатура выбора какие логи выгружать
sendLogs_warning = KeyboardButton('Предупреждения WARNING')
sendLogs_error = KeyboardButton('Ошибки ERROR')
sendLogs_kb = ReplyKeyboardMarkup(resize_keyboard=True)
sendLogs_kb.add(sendLogs_warning).add(sendLogs_error)
