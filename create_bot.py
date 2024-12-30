from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = 'BOT_TOKEN'
ADMIN_ID = int("ID_USER")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
