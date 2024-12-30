from bot_telega.create_bot import bot
from bot_telega.database.connect import sql_start, get_order
from bot_telega.create_bot import ADMIN_ID

async def get_question(username, question):
    await bot.send_message(ADMIN_ID, f"❓<b>Вопрос от @{username}:</b>\n{question}", parse_mode="html")

async def order_notification(username):
        sql_start()
        order_info = await get_order(username)
        await bot.send_message(ADMIN_ID, f'🗒 <b>Внимание! Новый заказ!</b>\n'
                                f'\n'
                                f'Клиент: <b>{order_info[0][0]}</b>\n'
                                f'ID-Клиента: <b>{order_info[0][1]}</b>\n'
                                f'Заказ: <b>{order_info[0][2]}</b>\n'
                                f'Статус оплаты заказа: <b>{order_info[0][3]}\n</b>'
                                f'Сумма заказа: <b>{order_info[0][4]}</b>\n'
                                f'Способ оплаты заказа: <b>{order_info[0][5]}</b>\n'
                                f'Адрес клиента: <b>{order_info[0][6]}</b>\n'
                                f'Номер телефона клиента: <b>{order_info[0][6]}</b>\n'
                                f'\n'
                                f'‼️ Скорее примите заказ!', parse_mode="html")
