import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app import keyboards as kb
from app import database as db
from dotenv import load_dotenv
import os

storage = MemoryStorage()
load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot, storage=storage)


# Зпускаем бд
async def on_startup(_):
    await db.db_start()
    print("Бот и БД успешно запушены")


# Создаем класс состояний товаров
class newOrder(StatesGroup):
    type = State()
    name = State()
    desc = State()
    price = State()
    photo = State()
    #size = State()


# Приветственно сообщение и проверка на администратора
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await db.cmd_start_db(message.from_user.id)
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в наш магазин!')
    await message.answer_sticker('CAACAgIAAxkBAAIMYGYw1kd5X7S5FfzQteEEdpg41lliAAKHAgACVp29CkLtdCtAV9CQNAQ',
                                 reply_markup=kb.main)
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор!', reply_markup=kb.main_admin)


# Главное меню
@dp.message_handler(text='Каталог')
async def contacts(message: types.Message):
    await message.answer("Наш каталог", reply_markup=kb.catalog_list)


# Обработчик кнопки "Корзина"
@dp.message_handler(text='Корзина')
async def show_cart(message: types.Message):
    user_id = message.from_user.id
    cart_items = await db.get_cart_info(user_id)
    if cart_items:
        for item in cart_items:
            # Формируем текст сообщения на основе данных из базы данных
            message_text = f"Футболка: {item[1]}\nОписание: {item[2]}\nЦена: {item[3]}"
            # Отправляем сообщение пользователю с фото и без инлайн клавиатуры
            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=item[4],
                caption=message_text
            )
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Ваша корзина пуста.")


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer("Наши контакты ------")
# Главное меню


# Если админ то показывем другую клавиатуру
@dp.message_handler(text='Админ-панель')
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer("Вы вошли в админ-панель", reply_markup=kb.admin_panel)
    else:
        await message.reply('Нет доступа к админ-панели')


# Проверяем еще раз на администратора и начинаем процесс добавления товара
@dp.message_handler(text='Добавить товар')
async def add_item(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await newOrder.type.set()
        await message.answer(f'Выберите тип товара', reply_markup=kb.catalog_list)
    else:
        await message.reply('Я вас не понимаю')


# Добавление типа товара
@dp.callback_query_handler(state=newOrder.type)
async def add_item_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
    await call.message.answer(f'Название товара')
    await newOrder.next()


# Добавление имени товара
@dp.message_handler(state=newOrder.name)
async def add_item_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(f'Описнаие товара')
    await newOrder.next()


# Добавление описания товара
@dp.message_handler(state=newOrder.desc)
async def add_item_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await message.answer(f'Введите цену товара')
    await newOrder.next()


# Добавление стоимости товара
@dp.message_handler(state=newOrder.price)
async def add_item_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer(f'Пришлите фото товара')
    await newOrder.next()


# Проверяем было ли действительно отправлено фото
@dp.message_handler(lambda message: not message.photo, state=newOrder.photo)
async def add_item_photo_check(message: types.Message):
    await message.answer("Это не фото!")


# Добавление фото товара
@dp.message_handler(content_types=['photo'], state=newOrder.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await db.add_items(state)
    await message.answer(f'Товар успешно создан!', reply_markup=kb.admin_panel)
    await state.finish()


# Обработчик неизвестных команд
@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я Вас не понимаю')


# Функция добавлеения в крзину
@dp.callback_query_handler(lambda query: query.data.startswith('add_to_cart:'))
async def add_to_cart_handler(callback_query: types.CallbackQuery):
    print("Приходит")
    # Извлекаем i_id товара из данных коллбэка
    i_id = int(callback_query.data.split(':')[1])

    # Получаем tg_id пользователя
    tg_id = callback_query.from_user.id

    # Записываем i_id товара в таблицу accounts в столбец cart_id
    await db.add_to_cart(tg_id, i_id)

    # Отправляем сообщение о том, что товар добавлен в корзину
    await bot.send_message(chat_id=tg_id, text="Товар успешно добавлен в корзину!")


# Основаная клавиатура для каталога и добавления товара
@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery):
    if callback_query.data == 'Футболки':
        t_shirts = await db.choice_tshirt()
        if t_shirts:
            for t_shirt in t_shirts:
                # Формируем текст сообщения на основе данных из базы данных
                message_text = f"Футболка: {t_shirt[1]}\nОписание: {t_shirt[2]}\nЦена: {t_shirt[3]}"

                # Создаем инлайн клавиатуру для кнопки "Добавить в корзину"
                inline_keyboard = InlineKeyboardMarkup()
                inline_keyboard.add(
                    InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart:{t_shirt[0]}'))

                # Отправляем сообщение пользователю с фото и инлайн клавиатурой
                await bot.send_photo(
                    chat_id=callback_query.from_user.id,
                    photo=t_shirt[4],
                    caption=message_text,
                    reply_markup=inline_keyboard
                )
        else:
            await bot.send_message(chat_id=callback_query.from_user.id, text="К сожалению, футболки не найдены.")
    elif callback_query.data == 'Шорты':
        await bot.send_message(chat_id=callback_query.from_user.id, text="Вы выбрали Шорты")
    elif callback_query.data == 'Кроссовки':
        await bot.send_message(chat_id=callback_query.from_user.id, text="Вы выбрали кроссы")





# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
