from aiogram import F, types, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from others.states import User
from keyboards.inline_keyboards import inline_keyboard

fsm_router = Router()

@fsm_router.message(F.text == '🏠 Return to main page')
async def return_to_main_page(message: types.Message, state: FSMContext) -> None:
    await message.bot.send_chat_action(action=ChatAction.TYPING,
                                        chat_id=message.chat.id)
    
    data_language = await state.get_data()
    text = data_language.get('user')
    await message.answer(
        text=text
        )
    
@fsm_router.message(F.text == '🌏 Change language')
async def change_language(message: types.Message, state: FSMContext) -> None:
    await message.bot.send_chat_action(action=ChatAction.TYPING,
                                       chat_id=message.chat.id)
    await state.set_state(User.language)
    await message.reply(text='Select language',
                        reply_markup=inline_keyboard)
