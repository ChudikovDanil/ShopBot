import sqlite3 as sq

db = sq.connect('shop.db')
cur = db.cursor()


async def db_start():
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            address TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS items(
            i_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            desc TEXT,
            price TEXT,
            photo TEXT,
            brand TEXT)""")

    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id = ?", (user_id,)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES (?)", (user_id,))
        db.commit()
        # Создаем таблицу корзины для нового пользователя
        cur.execute(f"""CREATE TABLE IF NOT EXISTS cart_{user_id}(
            item_id INTEGER,
            FOREIGN KEY (item_id) REFERENCES items(i_id))""")
        db.commit()


async def add_items(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)",
                    (data['name'], data['desc'], data['price'], data['photo'], data['type']))
        db.commit()


async def add_addr(user_id, address):
    cur.execute("UPDATE accounts SET address = ? WHERE tg_id = ?", (address, user_id))
    db.commit()


async def get_address(user_id):
    cur.execute("SELECT address FROM accounts WHERE tg_id = ?", (user_id,))
    address = cur.fetchone()
    if address:
        return address[0]
    else:
        return None


async def choice_tshirt():
    t_shirts = cur.execute("SELECT * FROM items WHERE brand='Футболки'").fetchall()
    return t_shirts


async def add_to_cart(user_id, item_id):
    # Проверяем, существует ли таблица корзины пользователя, иначе создаем ее
    cur.execute(f"CREATE TABLE IF NOT EXISTS cart_{user_id} (item_id INTEGER)")
    db.commit()
    # Добавляем товар в корзину пользователя
    cur.execute(f"INSERT INTO cart_{user_id} (item_id) VALUES (?)", (item_id,))
    db.commit()


async def get_cart_info(user_id):
    try:
        # Проверяем существование таблицы cart_{user_id}
        cur.execute(f"SELECT 1 FROM cart_{user_id} LIMIT 1")
    except sq.OperationalError:
        # Если таблицы нет, возвращаем None
        return None

    # Если таблица существует, продолжаем выполнение запроса
    user_cart = cur.execute(f"SELECT item_id FROM cart_{user_id}").fetchall()
    if user_cart:
        # Извлекаем значения из кортежей
        item_ids = [str(item[0]) for item in user_cart]
        # Используем запятую для объединения ID товаров в строку
        items_str = ', '.join(item_ids)
        # Формируем запрос, используя строки с ID товаров
        cart_items = cur.execute(f"SELECT * FROM items WHERE i_id IN ({items_str})").fetchall()
        return cart_items
    else:
        return None


# Подсчет суммы товаров в корзине
async def total_sum(user_id):
    try:
        # Проверяем существование таблицы cart_{user_id}
        cur.execute(f"SELECT 1 FROM cart_{user_id} LIMIT 1")
    except sq.OperationalError:
        # Если таблицы нет, возвращаем сообщение о пустой корзине
        return "Ваша корзина пуста."

        # Если таблица существует, продолжаем выполнение запроса
    user_cart = cur.execute(f"SELECT item_id FROM cart_{user_id}").fetchall()
    if user_cart:
        # Извлекаем значения из кортежей
        item_ids = [str(item[0]) for item in user_cart]
        # Используем запятую для объединения ID товаров в строку
        items_str = ', '.join(item_ids)
        # Формируем запрос, используя строки с ID товаров
        cart_items = cur.execute(f"SELECT price FROM items WHERE i_id IN ({items_str})").fetchall()
        # Суммируем стоимость товаров
        total = sum([float(item[0]) for item in cart_items])
        return total
    else:
        return "Ваша корзина пуста."


# Удаление товара по id
async def delete(id_items):
    cur.execute("DELETE FROM items WHERE i_id = (?)", id_items)
    db.commit()


# Получение всех id
async def select_id():
    return cur.execute('SELECT tg_id FROM accounts').fetchall()


# Очистка корзины
async def clear_cart(user_id):
    cur.execute(f"DROP TABLE IF EXISTS cart_{user_id}")
    db.commit()



