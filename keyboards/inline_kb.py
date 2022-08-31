from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# кнопка создания платежа на 5 минут
paymentAmount_kb = InlineKeyboardMarkup(row_width=1)
getPayAmount = InlineKeyboardButton(text='Пополнить баланс', callback_data='getPaymentAmount')
paymentAmount_kb.add(getPayAmount)
