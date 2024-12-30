import sqlite3
from bot_telega.create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_telega.markup.markups import *

global base, cursor
base = sqlite3.connect("database.db")
cursor = base.cursor()


#create table in database "telegram"
def create_table():

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    userid INTEGER,
    order_text TEXT,
    order_status_paid TEXT,
    order_price INTEGER,
    pay_method TEXT,
    user_adress TEXT,
    delivery TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
    name_product TEXT,
    available INTEGER DEFAULT 1 NOT NULL,
    photo TEXT,
    price INTEGER
    )
    ''')

    base.commit()

#connecting to db and start operationgs
def sql_start():

    base = sqlite3.connect("telegram.db")
    cursor = base.cursor()

#making request to db for add a new user
def add_user(username, userid):
    cursor.execute('INSERT OR IGNORE INTO users (username, userid) VALUES (?, ?)', (username, userid))
    base.commit()

#making private infortmation about user like address and phone number
def add_private_info_user(phone_number, user_adress, username):
    cursor.execute('UPDATE "users" SET "phone_number" == ?, "user_adress" == ? WHERE "username" == ? ', (phone_number, user_adress, username,))
    base.commit()

def add_value(name_product, available):
    cursor.execute('UPDATE products SET available == ? WHERE name_product == ?', (name_product, available))
    base.commit()


#check if product are availalbe in catalogue
def checker():
    check = cursor.execute ('SELECT * FROM products WHERE available == 1 LIMIT 1').fetchone()
    base.commit()
    return check

#add new product to catalogue (admin-function)
async def add_product(name_product, photo, price):
    cursor.execute('INSERT INTO products (name_product, photo, price) VALUES (?, ?, ?)', (name_product, photo, price, ))
    base.commit()

#delete product from catalogue (admin-function)
async def del_product(name_product):
    cursor.execute('DELETE FROM products WHERE name_product == ?', (name_product,))
    base.commit()

#check sells from our hour (admin-function)
def get_info_sell():
    sells = cursor.execute('SELECT name_sell, available_sell, userid FROM sells').fetchmany()
    base.commit()
    return sells

def add_order(username, order_text, order_status_paid, order_price, pay_method, user_adress, phone_number, delivery):
    cursor.execute('UPDATE "users" SET "order_text" == ?, "order_status_paid" == ?, "order_price" == ?, "pay_method" == ?, "user_adress" == ?, "phone_number" == ?, "delivery" == ? WHERE username == ?', (order_text, order_status_paid, order_price, pay_method, user_adress, phone_number, delivery, username,))
    base.commit()

async def receive_method(user_address,delivery, username):
    cursor.execute('UPDATE "users" SET "user_adress" == ?, "delivery" == ? WHERE username == ? ',(user_address, delivery, username,))
    base.commit()

async def print_products(message, offset, limit, showed):
    for obj in cursor.execute(f"SELECT * FROM products WHERE available == 1 LIMIT {limit} OFFSET {offset}").fetchall():
        add_markup = InlineKeyboardMarkup(resize_keyboard = True, row_width = 1)
        shop_btn = InlineKeyboardButton(f"Купить '{obj[0]}'", callback_data = f"buy_sneak_{obj[0]}")
        add_markup.add(shop_btn)
        await bot.send_photo(message.chat.id, obj[2] , f'‎\n🥏 <b>{obj[0]}</b>\n\n🔹 Цена за кроссовки: {obj[3]}\n\n🔹', parse_mode="html", reply_markup = add_markup)
    row_counter = cursor.execute("SELECT COUNT(*) FROM products WHERE available == 1").fetchone()
    counter = row_counter[0]
    if counter > showed and counter != showed:
        await bot.send_message(message.chat.id, f"Показано <b>{showed}</b> кроссовок из <b>{counter}</b>", parse_mode='html', reply_markup = load_markup)
    elif counter < showed:
        await bot.send_message(message.chat.id, f"Показано <b>{counter}</b> кроссовок  из <b>{counter}</b>", parse_mode='html')
    else:
        await bot.send_message(message.chat.id, f"Показано <b>{showed}</b> кроссовок  из <b>{counter}</b>", parse_mode='html')

async def get_info(name):
    product = cursor.execute('SELECT name_product, price FROM products WHERE name_product == ?', (name,)).fetchmany()
    base.commit()
    return product


def get_info_user():
    users_id = cursor.execute('SELECT "userid" FROM users').fetchall()
    base.commit()
    return users_id

async def add_pay_method(method, username):
    cursor.execute('UPDATE users SET "pay_method" == ? WHERE "username" == ?', (method, username,))
    base.commit()

async def get_order(username):
    order = cursor.execute('SELECT "username", "userid", "order_text", "order_status_paid", "order_price", "pay_method", "user_adress", "phone_number", "delivery" FROM users WHERE username == ?', (username,)).fetchmany()
    base.commit()
    return order

