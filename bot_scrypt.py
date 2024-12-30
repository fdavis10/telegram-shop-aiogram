from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_telega.create_bot import bot, dp
from bot_telega.database.connect import sql_start, add_user, create_table, checker, print_products, add_order, receive_method, get_info, add_value, add_pay_method
from bot_telega.markup.markups import *
from bot_telega.admin.admin_panel import *
from bot_telega.admin.admin_functions_with_users import get_question, order_notification
import random

choices = []
final_price = 0
limit = 5
offset = 0
showed = limit
username = ""
remove_check = []
message_def = ""




class UserAddress(StatesGroup):
    user_address = State()

class Suggestion(StatesGroup):
    suggestion = State()

class Ask(StatesGroup):
    question = State()



@dp.message_handler(commands = ["start"])
async def start_command(message: types.Message):
    userid = message.from_id
    username = message.from_user.username
    sql_start()
    add_user(username, userid)
    await bot.send_message(message.chat.id, f'👟 Привествуем, вас в <b>POIDEL</b>⭐\n'
                                            f'\n'
                                            f'Мы - ваша надежная компания по доставке оригинальных кроссовок из Китая!🇨🇳✨'
                                            f'У нас вы найдете самые стильные и уникальные модели, которые подчеркнут ваш индвидуальный стиль.\n'
                                            f'\n'
                                            f'📦 Быстрая доставка, качественный сервис и лучшие цены -'
                                            f'все это ждет вас в <b>PODEL</b>\n'
                                            f'\n'
                                            f'Присоединяйтесь к нам и шагайте в мир моды с комфортом!🚀💙', parse_mode="html", reply_markup=main_markup)

@dp.message_handler(commands = ["choose_sneaker"])
async def choose_sneaker(message: types.Message):
    global offset, limit, showed,message_def
    offset = 0
    showed = limit
    sql_start()
    check = checker()
    message_def = message
    if check is not None:
        await bot.send_message(message.chat.id, "👟 Кроссовки в наличии:", reply_markup = order_markup)
        await print_products(message, offset, limit, showed)
        offset += limit
        showed += limit
    else:
        await bot.send_message(message.chat.id, "🎰 Скоро пополним наличие кроссовок! Ожидайте!")


@dp.message_handler(commands = ['basket'])
async def basket_command(message: types.Message):
    global choices
    basket_sneakers = ("\n"
                       "\n"
                       "👟").join(choices)
    if choices != []:
        await bot.send_message(message.chat.id,f"<b>Корзина: </b>\n"
                                   f"\n"
                                   f"👟 {basket_sneakers}\n"
                                   f"\n"
                                   f"<b>Общая сумма:</b> {final_price} ",
                                   parse_mode="html", reply_markup=basket_markup)
    if choices == []:
        await bot.send_message(message.chat.id, "❌ Корзина пуста")

@dp.message_handler(commands = ['home'])
async def home_command(message: types.Message):
    if choices == []:
        await bot.send_message(message.chat.id, "🏠 Вы вышли в главное меню<", reply_markup=main_markup)
    elif choices != []:
        await bot.send_message(message.chat.id, "🏠 Вы вышли в главное меню", reply_markup=basket_markup)


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    global offset, limit, showed, message_def, name, choices, remove_check

    if message.text == "👟 Выбрать кроссовки":
        offset = 0
        showed = limit
        sql_start()
        check = checker()
        message_def = message
        if check is not None:
            await bot.send_message(message.chat.id, "👟 Кроссовки в наличии:", reply_markup=order_markup)
            await print_products(message, offset, limit, showed)
            offset += limit
            showed += limit
        else:
            await bot.send_message(message.chat.id, "🎰 Скоро пополним наличие кроссовок! Ожидайте!")

    elif message.text == "🗑 Корзина":
        basket_sneakers = ("\n"
                           "\n"
                           "👟 ").join(choices)
        if choices != []:
            await bot.send_message(message.chat.id,
                                   f"<b>Корзина: </b>\n"
                                   f"\n"
                                   f"👟 {basket_sneakers}\n"
                                   f"\n"
                                   f"<b>Общая сумма:</b> {final_price} ",
                                   parse_mode="html", reply_markup=basket_markup)
        elif choices == []:
            await bot.send_message(message.chat.id, "❌ Корзина пуста")

    elif message.text == "🏠 Главное меню":
        if choices == []:
            await bot.send_message(message.chat.id, "🏠 Вы вышли в главное меню",
                                   reply_markup=main_markup)
        elif choices != []:
            await bot.send_message(message.chat.id, "🏠 Вы вышли в главное меню",
                                   reply_markup=main_markup)

    elif message.text == "🌀 О нас":
        await bot.send_message(message.chat.id,
                               f'Мы - ваша надежная компания по доставке оригинальных кроссовок из Китая!🇨🇳✨'
                               f'У нас вы найдете самые стильные и уникальные модели, которые подчеркнут ваш индвидуальный стиль.\n'
                               f'\n'
                               f'📦 Быстрая доставка, качественный сервис и лучшие цены -'
                               f'все это ждет вас в <b>PODEL</b>\n'
                               f'\n'
                               f'Присоединяйтесь к нам и шагайте в мир моды с комфортом!🚀💙',
                               parse_mode="html", reply_markup=main_markup)

    elif message.text == "✨ FAQ":
        await bot.send_message(message.chat.id,
                               "❓ Ответы на популярные вопросы\n"
                               "\n"
                               "💬 <b>Как мне забрать мой заказ?</b>\n"
                               "📢 Вы можете заказать доставку вашего заказа (платно), либо забрать его по адресу(бесплатно).\n"
                               "\n"
                               "💬 <b>Как проходит оплата заказа?</b>\n"
                               "📢 После того, как вы оформили заказ, вы можете выбрать способ оплаты: банковская карта, наличные. Оплата наличными принимается только при самовывозе. Вы сможете оплатить заказ банковской картой по ссылке, полученной от бота.\n"
                               "\n"
                               "💬 <b>Как мне вернуть заказ?</b>\n"
                               "📢Возврат заказа происходит по адресу: <b>г. Москва, ул. Новогиреевская 18/31</b>\n"
                               "\n"
                               "💬 <b>Нету информации по заказу, что делать?</b>\n"
                               "📢 Свяжитесь с ним напрямую, ссылка на чат в телеграмме: <b>@manager_podel</b>\n",
                               parse_mode="html", reply_markup=main_markup)

    elif message.text == "👨‍💻 Спросить":
        await Ask.question.set()
        await bot.send_message(message.chat.id, "📋 Введите интересующий вас вопрос", parse_mode="html")

    elif message.text == "✅ Оформить":
        username = message.from_user.username
        order_sneakers = ', '.join(choices)
        sql_start()
        add_order(f"{username}",order_sneakers, 0, f"{final_price}", "None", "None", "None", "None")
        await bot.send_message(message.chat.id, "🎯 Выберите метод получения заказа", reply_markup=pick_method_markup)

    elif message.text == "🚶‍♂️ Самовывоз":
        username = message.from_user.username
        await receive_method('Самовывоз', 'Самовывоз', username)
        await bot.send_message(message.chat.id, "🗺 Самовывоз с адреса:\n"
                                                "\n"
                                                "<b>г. Москва, ул. Новогиреевская 18/31</b>", parse_mode="html",
                               reply_markup=buy_markup)

    elif message.text == "🚘 Доставка":
        await UserAddress.user_address.set()
        await bot.send_message(message.chat.id, '📥 Укажите адрес на который будет произведена доставка')


    elif message.text == "✅ Оплатить":
        await bot.send_message(message.chat.id, "Выберите способ оплаты:", reply_markup=pay_method)

    elif message.text == "💳 Банковская карта":
        sql_start()
        username = message.from_user.username
        await add_pay_method("Банковская карта", username)
        await bot.send_message(message.chat.id, f'💸 <b>Ваш чек на оплату</b>\n'
                                                f''
                                                f'\n'
                                                f'💳 У вас есть <b>15</b> минут для оплаты указанного товара на сумму: <b>{final_price}</b>\n'
                                                f'Если у вас возникли вопросы по оплате - используйте контакт менеджера: <b>@manager_podel</b>\n'
                                                f'\n'
                                                f'‼️ <b>Внимание!</b>\n'
                                                f'\n'
                                                f'Наш менеджер никогда не напишет вам с просьбой перевода денег на какой-либо счет!\n'
                                                f'Внимательно сверяйте указанный контакт с контактом, который вам написал!\n'
                                                f'Все вопросы вы можете задать прямо через бота!\n'
                                                f'\n'
                                                f'\n'
                                                f'🛍🎉 Приятных покупок, с уважанием команда <b>PODEL</b>', parse_mode="html")

    elif message.text == "💵 Наличными":
        sql_start()
        username = message.from_user.username
        await add_pay_method("Наличными", username)
        await bot.send_message(message.chat.id, f'💸 <b>Вы выбрали оплату за наличные</b>\n'
                                                f'\n'
                                                f'🚘 Если вы выбрали <b>доставку</b> - приготовьте наличные на сумму\n'
                                                f'{final_price} и при получении игры вручите их нашему курьеру!\n'
                                                f'\n'
                                                f'🚶‍♂️ Если вы выбрали <b>самовывоз</b>, вручите наличные на сумму {final_price}\n'
                                                f'Нашему оператору и забирайте игру!', parse_mode="html", reply_markup=cash_markup)

    elif message.text == "✅ Подтвердить":
        username = message.from_user.username
        await bot.send_message(message.chat.id, "✅ Ваш заказ принят, скоро с вами свяжется продавец",
                               reply_markup=main_markup)
        await order_notification(username)
        choices = []

    elif message.text == "📤 Убрать из корзины":
        choices_ind = 0
        remove_markup = InlineKeyboardMarkup(resize_keyboard = True)
        for item in choices:
            sneak_name = item.split(" -")[0]
            rem_button = InlineKeyboardButton(f"Убрать '{sneak_name}'",
                                                  callback_data=f"rem_{sneak_name}i{choices_ind}")
            remove_markup.add(rem_button)
            remove_check.append(sneak_name)
            choices_ind += 1
        await bot.send_message(message.chat.id, "Что убрать?", reply_markup= remove_markup)



@dp.callback_query_handler(lambda c: c.data.startswith("buy_sneak_"))
async def add_to_basket(callback: types.CallbackQuery):
    global final_price, offset, limit, showed

    if callback.data.startswith("buy_sneak_"):
        if callback.data.replace("buy_sneak_", "") not in choices:
            sql_start()
            product = await get_info(callback.data.replace("buy_sneak_", ""))
            await callback.answer(text = f'Кроссовки "{product[0][0]}" добавлены в вашу корзину')
            choices.append(product[0][0])
            final_price += product[0][1]
            add_value(product[0][0], 0)

@dp.message_handler(state = Ask.question)
async def question_register(message: types.Message, state: Suggestion.suggestion):
    username = message.from_user.username
    question = message.text
    await bot.send_message(message.chat.id, "✳️ Ваш вопрос сохранен и отправлен продавцу\n"
                                            "\n"
                                            "👨‍👩‍👦 Ожидайте ответа от продавца в личных сообщениях!", reply_markup=main_markup)
    await get_question(username, question)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data)
async def load_more(callback: types.CallbackQuery):
    global message_def, offset, limit, showed
    if callback.data == "load_more":
        await print_products(message_def, offset, limit, showed)
        offset += limit
        showed += limit

@dp.message_handler(state = UserAddress.user_address)
async def set_address(message: types.Message, state: UserAddress.user_address):
    username = message.from_user.username
    address = message.text
    await bot.send_message(message.chat.id, f'📦 Доставка оплачивается отдельно!\n'
                                            f'В пределах г. Москва - <b>350</b> рублей\n'
                                            f'За каждый киллометр от МКАДА + <b>150</b> рублей\n'
                                            f'\n'
                                            f'🚗 Доставка будет произведена на данный адрес: <b>{address}</b>',
                           parse_mode="html", reply_markup=buy_markup)
    await receive_method(address, 1, username)
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.startswith(f"rem_{sneak_name}i{choices_ind}"))
async def remove_from_basket(callback: types.CallbackQuery):
    global final_price,offset, limit, showed
    if callback.data.startswith("rem_"):
        basket_name = callback.data.replace("rem_", "")
        sneak_name_ind = basket_name.split(" -")[0]
        choices_index = sneak_name_ind.split("i")[1]
        sneak_name = sneak_name_ind.split("i")[0]
        if sneak_name in remove_check:
            sql_start()
            product = await get_info(sneak_name)
            await callback.answer(text=f"Кроссовки '{sneak_name}' убраны из корзины")
            remove_check.remove(sneak_name)
            choices.pop(int(choices_index))
            final_price -= product[0][1]
            add_value(sneak_name, 1)