from aiogram import Dispatcher, Bot

from database.db import create_database, create_table, cnn_pool
from routers.main_routers import main_router
from others.cfg import log
from tokens import api_key

import asyncio

dspt = Dispatcher()
dspt.include_router(
    main_router
)   

async def main():
    pool = await cnn_pool()
    await create_database(pool)
    await create_table(pool)
    try:
        bot = Bot(
            token=api_key
            )
        await dspt.start_polling(bot)
    except KeyboardInterrupt:
        await pool.close()
        await pool.wait_closed()
        log('Code was completed!') 
    
if __name__ == "__main__":
    asyncio.run(main())
