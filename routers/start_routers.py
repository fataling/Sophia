from aiogram import types, Router
from aiogram.filters import Command
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramConflictError, TelegramBadRequest

from keyboards.inline_keyboards import inline_keyboard
from others.stickers import stickers
from others.states import User
from others.cfg import log

import random

start_router = Router()

async def handler_user_state(state: FSMContext) -> int | None:
    language_user = await state.get_data()
    
    if language_user != {}:
        text_language = language_user.get('user')
        return text_language
    else:
        return None
    
async def handler_message_page(message: types.Message, state: FSMContext, text_language) -> None:
    stick_id = random.choice(stickers)
    
    try:
        await message.answer_sticker(
            sticker=stick_id
            )
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=message.chat.id)
        
        if text_language != None:
            await message.answer(
                text=text_language
                )
        else:
            await state.set_state(User.language)
            await message.answer(text='💬 Select language',
                                 reply_markup=inline_keyboard)
    except TelegramConflictError as a:
        log(f'This bot launched somewhere else! - {a}')
    except TelegramBadRequest as b:
        log(f'Request was declined a Telegram! - {b}')
 
@start_router.message(Command("start", prefix='/!'))
async def handler_start(message: types.Message, state: FSMContext):
    data = await handler_user_state(state)
    await handler_message_page(message, state, data)
