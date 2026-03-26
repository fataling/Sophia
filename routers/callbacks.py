from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from others import greetings
from others.states import User
from keyboards.reply_keyboards import reply_keyboard

callback_router = Router()

@callback_router.callback_query(F.data == 'lang_en', User.language)
async def language_english(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(user=greetings.en)
    await callback.message.delete()
    
    await callback.message.bot.send_chat_action(action=ChatAction.TYPING,
                                                chat_id=callback.message.chat.id)
    await callback.message.answer(text=greetings.en,
                                  reply_markup=reply_keyboard)
        
@callback_router.callback_query(F.data == 'lang_ru', User.language)
async def language_english(callback: CallbackQuery, state: FSMContext) -> None: 
    await state.update_data(user=greetings.ru)
    await callback.message.delete()
    
    await callback.message.bot.send_chat_action(action=ChatAction.TYPING,
                                                chat_id=callback.message.chat.id)
    await callback.message.answer(text=greetings.ru,
                                  reply_markup=reply_keyboard)
        
@callback_router.callback_query(F.data == 'lang_zh', User.language)
async def language_english(callback: CallbackQuery, state: FSMContext) -> None: 
    await state.update_data(user=greetings.zh) 
    await callback.message.delete()
    
    await callback.message.bot.send_chat_action(action=ChatAction.TYPING,
                                                chat_id=callback.message.chat.id)
    await callback.message.answer(text=greetings.zh,
                                  reply_markup=reply_keyboard)
        
@callback_router.callback_query(F.data == 'lang_jp', User.language)
async def language_english(callback: CallbackQuery, state: FSMContext) -> None: 
    await state.update_data(user=greetings.jp)
    await callback.message.delete()
    
    await callback.message.bot.send_chat_action(action=ChatAction.TYPING,
                                                chat_id=callback.message.chat.id)
    await callback.message.answer(text=greetings.jp,
                                  reply_markup=reply_keyboard)
