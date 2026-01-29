from asyncio.exceptions import CancelledError
from routers.main_routers import main_router
from aiogram import Dispatcher, Bot
from tokens import api_key
from others.cfg import log

from database.db import connector_to_server, create_database, create_table

import asyncio

bot = Bot(token=api_key)

dspt = Dispatcher()
dspt.include_router(
    main_router
)

async def main():
    connect = await connector_to_server()
    await create_database(connect)
    await create_table(connect)
    try:
        await dspt.start_polling(bot)
    except KeyboardInterrupt:
        log('Code was completed!')
    
if __name__ == "__main__":
    asyncio.run(main())
