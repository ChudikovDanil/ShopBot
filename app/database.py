import sqlite3 as sq

db = sq.connect('shop.db')
cur = db.cursor()


async def db_start():
    cur.execute("""CREATE TABLE IF NOT EXISTS accounts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER,
            cart_id INTEGER,
            FOREIGN KEY (cart_id) REFERENCES items(i_id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS items(
        i_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        desc TEXT,
        price TEXT,
        photo TEXT,
        brand TEXT)""")

    db.commit()


# собираем id пользователей
async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()


async def add_items(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO items (name, desc, price, photo, brand) VALUES (?, ?, ?, ?, ?)",
                    (data['name'], data['desc'], data['price'], data['photo'], data['type']))
        db.commit()


async def choice_tshirt():
    t_shirts = cur.execute("SELECT * FROM items WHERE brand='Футболки'").fetchall()
    return t_shirts


async def add_to_cart(user_id, i_id):
    # Записываем i_id товара в таблицу accounts в столбец cart_id
    cur.execute("UPDATE accounts SET cart_id = ? WHERE tg_id = ?", (i_id, user_id))
    db.commit()


# Функция для получения информации о товарах в корзине
async def get_cart_info(user_id):
    user_cart = cur.execute("SELECT cart_id FROM accounts WHERE tg_id = ?", (user_id,)).fetchone()
    if user_cart:
        cart_items = cur.execute("SELECT * FROM items WHERE i_id IN ({})".format(','.join(map(str, user_cart)))).fetchall()
        return cart_items
    else:
        return None