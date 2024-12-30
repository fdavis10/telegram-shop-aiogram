from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from bot_telega.create_bot import bot, dp
from bot_telega.database.connect import sql_start, add_product, del_product, add_value, get_info_user, get_order
from bot_telega.markup.markups import (admin_markup, sub_res_markup,main_markup)
from bot_telega.create_bot import ADMIN_ID




message_def = ""

class AddSneaker(StatesGroup):
    name = State()
    price = State()
    photo = State()

class SetAvailable(StatesGroup):
    sneaker_name = State()

class DeleteSneaker(StatesGroup):
    sneaker_name_del = State()

class Notification(StatesGroup):
    message_notification = State()

sneak_info = {}

# admin panel activation
@dp.message_handler(commands=["apanel"])
async def authorization_admin(message: types.Message):
    global ADMIN_ID
    ID = message.from_user.id
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(message.from_user.id, "🛠 Вы авторизовались в админ панель", reply_markup=admin_markup)
        await message.delete()
    else:
        await bot.send_message(message.chat.id, "❌ У вас нет доступа к админ панели", reply_markup=main_markup)

@dp.message_handler(lambda message: "Добавить новые кроссовки" in message.text, state = None)
async def adm_start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await AddSneaker.name.set()
        await bot.send_message(message.chat.id, "Введи название кроссовок")

@dp.message_handler(state = AddSneaker.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID or ADMIN_EVA:
        async with state.proxy() as data:
            data['name_product'] = message.text
        await AddSneaker.next()
        await bot.send_message(message.chat.id, "Теперь введите цену за кроссовки")

@dp.message_handler(state = AddSneaker.price)
async def load_price_day(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await AddSneaker.next()
        await bot.send_message(message.chat.id, "Теперь загрузите фото")

@dp.message_handler(content_types = ["photo"], state = AddSneaker.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        global sneak_info
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        async with state.proxy() as data:
            await bot.send_message(message.chat.id, "Введенная информация:", reply_markup = sub_res_markup)
            await bot.send_message(message.chat.id, f"Название: {data['name_product']}\nЦена кроссовок: {data['price']}\n")
            await bot.send_photo(message.chat.id, data['photo'])
            sneak_info = data
        await state.finish()

@dp.message_handler(lambda message: "Добавить" in message.text)
async def add_products(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        global sneak_info
        if sneak_info != {}:
            sql_start()
            await add_product(sneak_info['name_product'],sneak_info['photo'], sneak_info['price'])
            await bot.send_message(message.chat.id, "Кроссовки добавлены в базу данных", reply_markup = admin_markup)
        elif sneak_info == {}:
            await bot.send_message(message.chat.id, "Сначала введите данные о кроссовках")

@dp.message_handler(lambda message: "Сбросить" in message.text)
async def reset_info(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await bot.send_message(message.chat.id, "Изменения сброшены", reply_markup = admin_markup)

@dp.message_handler(lambda message: "Удалить кроссовки" in message.text)
async def delete_product(message: types.Message):
    await DeleteSneaker.sneaker_name_del.set()
    await bot.send_message(message.chat.id, "Введите название кроссовок, которые нужно удалить")

@dp.message_handler(state = DeleteSneaker.sneaker_name_del)
async def delete_game_db(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        name_product = message.text
        sql_start()
        await del_product(name_product)
        await bot.send_message(message.chat.id, f"Кроссовки <b>'{name_product}'</b> удалены из базы данных", parse_mode="html")
        await state.finish()

@dp.message_handler(lambda message: "Вернуть в наличие" in message.text)
async def set_av_name(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await SetAvailable.sneaker_name.set()
        await bot.send_message(message.chat.id, "Введите название кроссовок, которой нужно вернуть статус <b>'В наличие'</b>", parse_mode="html")

@dp.message_handler(state = SetAvailable.sneaker_name)
async def set_av(message: types.Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        async with state.proxy() as name:
            name["name_product"] = message.text
            sql_start()
            add_value(name["name_product"], 1)
            await bot.send_message(message.chat.id, f"Кроссовки '{name['name_product']}' теперь снова в наличии!")
        await state.finish()

@dp.message_handler(lambda message: "📢 Оповестить пользователей" in message.text)
async def notification_users(message: types.Message):
    if message.chat.id == ADMIN_ID:
        await bot.send_message(message.chat.id, '🔔 Введите новость, которую хотите опубликовать:')
        await Notification.message_notification.set()

@dp.message_handler(state = Notification.message_notification)
async def handle_message_for_notifications(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN_ID:
        message_notificataion = message.text
        users_id = get_info_user()
        for usid in users_id:
            await bot.send_message(chat_id=usid[0], text = f'🛠 Оповещение от администратора!\n'
                                                           f'\n'
                                                           f'{message_notificataion}')
        await bot.send_message(message.chat.id, '🟢 Новость отправлена всем пользователям!')
        await state.finish()