from aiogram import Dispatcher, Bot

from database.db import sql_create_database, sql_create_table, sql_create_pool
from routers.main_routers import main_router
from others.cfg import log
from tokens import api_key

import asyncio

dspt = Dispatcher()
dspt.include_router(
main_router
)   
    
async def main():
    pool = await sql_create_pool()
    await sql_create_database(pool)
    await sql_create_table(pool)
    
    dspt['pool'] = pool
    
    try:
        bot = Bot(
            token=api_key
            )
        await dspt.start_polling(bot)
    except KeyboardInterrupt:
        log('Code was completed!') 
        await pool.close()
        await pool.wait_closed()
    
if __name__ == "__main__":
    asyncio.run(main())
