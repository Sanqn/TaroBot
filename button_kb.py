from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

buttons = [
    InlineKeyboardButton(text='Овен', callback_data='Овен'),
    InlineKeyboardButton(text='Телец', callback_data='Телец'),
    InlineKeyboardButton(text='Близнецы', callback_data='Близнецы'),
    InlineKeyboardButton(text='Рак', callback_data='Рак'),
    InlineKeyboardButton(text='Лев', callback_data='Лев'),
    InlineKeyboardButton(text='Дева', callback_data='Дева'),
    InlineKeyboardButton(text='Весы', callback_data='Весы'),
    InlineKeyboardButton(text='Скорпион', callback_data='Скорпион'),
    InlineKeyboardButton(text='Стрелец', callback_data='Стрелец'),
    InlineKeyboardButton(text='Козерог', callback_data='Козерог'),
    InlineKeyboardButton(text='Водолей', callback_data='Водолей'),
    InlineKeyboardButton(text='Рыбы', callback_data='Рыбы')
]

kb_inline_call = InlineKeyboardMarkup().add(*buttons)