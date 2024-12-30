from bot_telega.create_bot import dp
from aiogram import executor

from bot_telega.admin import admin_panel
import bot_telega.bot_scrypt

import tracemalloc

from bot_telega.database.connect import create_table

create_table()
tracemalloc.start()
executor.start_polling(dp)