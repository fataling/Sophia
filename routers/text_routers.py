from aiogram.enums import ChatAction
from aiogram import types, Router, F
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError

from others.cfg import model, client, log
from openai import InternalServerError, APITimeoutError
from database.db import sql_cnn_pool, sql_get_table, sql_include_table, Pool

text_router = Router()

async def handler_message_from_user(message: types.Message, pool: Pool) -> int:
    user_id = message.from_user.id
    data = await sql_get_table(pool,
                                user_id)
    
    if len(data) < 1:
        content = 'I am a helpful assistant a Sophia'
        await sql_include_table(pool,
                                user_id,
                                'system',
                                content)
    return user_id

async def handler_create_history_with_user(message: types.Message, pool: Pool, user_id: int):
    user_request = message.text
    await sql_include_table(pool,
                            user_id,
                            'user',
                            user_request)
    
async def handler_thinking_answer(message: types.Message) -> types.Message:
    await message.bot.send_chat_action(action=ChatAction.TYPING,
                                       chat_id=message.chat.id)
    thinking = await message.answer(
        text=f'Thinking...'
        )
    return thinking

async def handler_create_context_window(pool: Pool, user_id: int) -> list:
    raw_context = []
    data = await sql_get_table(pool,
                                user_id)
    for role, content in data:
        raw_context.append({'role': role,
                            'content': content})
    
    context = raw_context[::-1]
    if context != None:
        raw_context.clear()
        return context
    
async def handler_create_response(message: types.Message, context: dict) -> types.Message | None:
    try:
        model_response = client.responses.create(model=model,
                                                 input=context,
                                                 stream=False)
        assistant_response = model_response.output_text
        
        if assistant_response != None:
            return assistant_response
    except InternalServerError as a:
        await message.reply(
            text=f'Service is overloaded now, try again later! - {a}'
            )
        return None
    except APITimeoutError as b:
        await message.reply(
            text=f'Server not reply for your request, please try again! - {b}'
                )
        return None

async def handler_assistant_update_data(pool: Pool, assistant_response: str, user_id: int) -> None:
    await sql_include_table(pool,
                            user_id,
                            'assistant',
                            assistant_response)
        
async def handler_message_chat(message: types.Message, assistant_response: str, thinking: str) -> None:
    try:
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                           chat_id=message.chat.id)
        await thinking.edit_text(
            text=assistant_response
        )
    except TelegramAPIError as a:
        log(f'An error occurred while receiving a response from Telegram! - {a}')
    except TelegramForbiddenError as b:
        log(f'This bot is blocked, change a bot! - {b}')
        
@text_router.message(F.photo)
async def photo_handler(message: types.Message) -> None:
    await message.reply(
        text="I don't understand the photo yet, lets communicate in text!"
        )
    
@text_router.message(F.sticker)
async def sticker_handler(message: types.Message) -> None:
    await message.reply(
        text="i also use sticker, but now want read text!"
        )
    
@text_router.message(F.document)
async def document_handler(message: types.Message) -> None:
    await message.reply(
        text="I don't like a document, i like text!"
        )
    
@text_router.message(F.audio)
async def audio_handler(message: types.Message) -> None:
    await message.reply(
        text="The audio is still too complicated for me, tell me your thoughts!"
        )
    
@text_router.message(F.video)
async def video_handler(message: types.Message) -> None:
    await message.reply(
        text="What is video? I know only text!"
        )

@text_router.message(F.voice)
async def video_handler(message: types.Message) -> None:
    await message.reply(
        text="Voice? What? Only text message!"
        )
    
@text_router.message(F.text)
async def text_handler(message: types.Message) -> None:
    pool = await sql_cnn_pool()
    
    message_user = await handler_message_from_user(message, pool)
    
    await handler_create_history_with_user(message, pool, message_user)
    
    thinking = await handler_thinking_answer(message)
    
    context = await handler_create_context_window(pool, message_user)
    
    request_to_model = await handler_create_response(message, context)
    
    await handler_assistant_update_data(pool, request_to_model, message_user)
    
    await handler_message_chat(message, request_to_model, thinking)
