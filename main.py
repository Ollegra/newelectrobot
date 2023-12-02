# aiogram==3.0.0b7
# pip install python-dotenv
import asyncio
import logging
from backg import keep_alive
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from bot_db import db_start
#from config import TOKEN_API
import os
import dotenv
import locale


locale.setlocale(locale.LC_ALL, '')

dotenv.load_dotenv()

db_start()

async def main():
    bot = Bot(token=os.getenv('TOKEN_API'), parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

#keep_alive()
if __name__ == '__main__':
  
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.INFO, format='%(asctime)s : %(name)s : %(levelname)s : %(message)s', encoding='UTF-8')
    
    asyncio.run(main())

