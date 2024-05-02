from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для пользователя
main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог')
main.add('Корзина')
main.add('Контакты')

# Клавиатура для админа
main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог')
main_admin.add('Корзина')
main_admin.add('Контакты')
main_admin.add('Админ-панель')

# Панель администратора
admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')

# Инлайн клава для каталога
catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Футболки', callback_data='Футболки'),
                 InlineKeyboardButton(text='Шороты', callback_data='Шорты'),
                 InlineKeyboardButton(text='Кроссовки', callback_data='Кроссовки'))

cancel = ReplyKeyboardMarkup(resize_keyboard=True)
cancel.add('Отмена')

