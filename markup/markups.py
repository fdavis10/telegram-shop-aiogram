from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# creating button for back to main menu and button for choosing product
menu_btn = KeyboardButton("🏠 Главное меню")
choose_btn = KeyboardButton("👟 Выбрать кроссовки")


# create kb for main menu
about_btn = KeyboardButton("🌀 О нас")
faq_btn = KeyboardButton("✨ FAQ")
ask_btn = KeyboardButton("👨‍💻 Спросить")

# adding all kb buttons to main menu kb
main_markup = ReplyKeyboardMarkup(resize_keyboard = True).add(about_btn, faq_btn, ask_btn, choose_btn)

# create and add basket button and button "remove from busket"
basket_btn = KeyboardButton("🗑 Корзина")
basket_remove_btn = KeyboardButton("📤 Убрать из корзины")

order_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(basket_btn, menu_btn)

# creating buy button
buy_btn = KeyboardButton("✅ Оформить")

# creating order menu
basket_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(basket_remove_btn, basket_btn, menu_btn, choose_btn, buy_btn)
choice_basket_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(choose_btn, menu_btn, basket_btn)

# creating button "load more"
load_more = InlineKeyboardButton("♻️ Показать еще", callback_data="load_more")
# add to inline kb
load_markup = InlineKeyboardMarkup(resize_keyboard = True).add(load_more)

# creating different pick ups for products buttons
pickup = KeyboardButton("🚶‍♂️ Самовывоз")
delivery = KeyboardButton("🚘 Доставка")
# creating pick ups markup
pick_method_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(pickup, delivery, menu_btn)

# creating buy buttons
pay_bnt = KeyboardButton("✅ Оплатить")
# creating buy markup
buy_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(pay_bnt, basket_btn, menu_btn)

# REMOVE MARKUP
remove_markup = ReplyKeyboardMarkup(resize_keyboard=True)

# add pay methods buttons
card_btn = KeyboardButton("💳 Банковская карта")
cash_btn = KeyboardButton("💵 Наличными")
# add payment markup
pay_method = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(card_btn, cash_btn)

# add finaly buttons before orders submit
submit_btn = KeyboardButton("✅ Подтвердить")
change_btn = KeyboardButton("🔁 Изменить метод оплаты")
#adding markup before final order's submint with cash payment method
cash_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width=1).add(submit_btn, change_btn, menu_btn)

# adding return available button
available_btn = KeyboardButton("🔄 Вернуть в наличие")
# adding add new game to db
add_new = KeyboardButton("📦 Добавить новые кроссовки")
# adding delete game from db button
del_game_btn = KeyboardButton("❌ Удалить кроссовки")
# addint notification users
not_user_but = KeyboardButton("📢 Оповестить пользователей")

# adding admin markup
admin_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2).add(available_btn, add_new, del_game_btn, not_user_but, menu_btn)

# adding submit adding new game to db
sub_add_btn = KeyboardButton("✅ Добавить")
reset_btn = KeyboardButton("❌ Сбросить")

# adding submit or reset all info about new game
sub_res_markup = ReplyKeyboardMarkup(resize_keyboard = True, row_width = 2).add(sub_add_btn, reset_btn, menu_btn)
