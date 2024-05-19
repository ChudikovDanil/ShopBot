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
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку').add('Выйти в главное меню')

# Инлайн клава для каталога
catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Футболки', callback_data='Футболки'),
                 InlineKeyboardButton(text='Шороты', callback_data='Шорты'),
                 InlineKeyboardButton(text='Кроссовки', callback_data='Кроссовки'))


# Создание клавиатуры для очистки корзины
clear_cart_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
clear_cart_keyboard.add('Очистить корзину')
# Клавиатура для оформления заказа
clear_cart_keyboard.add('Оформить заказ')
clear_cart_keyboard.add('Выйти в главное меню')

# Кнопка для оплаты товара
pay_items = ReplyKeyboardMarkup(resize_keyboard=True)
pay_items.add("Оплатить товар")
pay_items.add("Вернуться в корзину")  # надо сделать обработчик

# Кнопка да
btn_yes = ReplyKeyboardMarkup(resize_keyboard=True)
btn_yes.add('Да', 'Нет')


# Кнопка для отмены удаления товара
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add('Отмена')

# Кнопка для отмены платежа
cancel_payment = ReplyKeyboardMarkup(resize_keyboard=True).add('Отменить платеж')
