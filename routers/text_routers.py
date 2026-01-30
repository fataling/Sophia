from aiogram.enums import ChatAction, ParseMode
from aiogram import types, Router, F
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError

from others.cfg import model, client, log
from database.roles import user, assistant
from openai import AuthenticationError, InternalServerError, APITimeoutError
from database.db import connector_to_server, include_in_table, select_data_from_table

text_router = Router()

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

async def handler_user_request_update_data(message: types.Message):
    connect = await connector_to_server()
    user_id = message.from_user.id
    user_request = message.text
    
    await include_in_table(connect,
                           user_id,
                           user,
                           user_request)
    
async def handler_thinking_process(message: types.Message):
    await message.bot.send_chat_action(action=ChatAction.TYPING,
                                       chat_id=message.chat.id)
    thinking = await message.answer(
        text='Thinking...'
        )
    return thinking
    
async def handler_create_context(message: types.Message):    
    user_id = message.from_user.id
    
    connect = await connector_to_server()
    data = await select_data_from_table(connect,
                                        user_id)
    raw_context = []
    for role, content in data:
        raw_context.append({'role': role,
                            'content': content})
    context = raw_context[::-1]
    return context

async def request_to_model(context):
    text = client.responses.create(model=model,
                                   input=context,
                                   stream=False)
    return text

@text_router.message(F.text)
async def handler_response_bot(message: types.Message) -> None:
    try:
        await handler_user_request_update_data(message)
        thinking = await handler_thinking_process(message)
        context = await handler_create_context(message)
        text = client.responses.create(model=model,
                                       input=context,
                                       stream=False)
        response = text.output_text
        await message.bot.send_chat_action(action=ChatAction.TYPING,
                                         chat_id=message.chat.id)
        await thinking.edit_text(response)
    except AuthenticationError as a:
       log(f'Your API token is incorrect, replace his! - {a}')
    except InternalServerError as b:
        log(f'Server is overloaded, try again... - {b}')
        await message.reply(
            text='Service is overloaded now, try again later!'
            )
    except APITimeoutError as c:
        log(f'Server not answers, waiting... - {c}')
        await message.reply(
            text='Server not reply for your request, please try again!'
            )
    except TelegramAPIError as d:
        log(f'An error occurred while receiving a response from Telegram! - {d}')
    except TelegramForbiddenError as e:
        log(f'This bot is blocked, change a bot! - {e}')
        
async def handler_assistant_request_update_data(message: types.Message, assistant: str, user_id: int, response: str, connect):
    await include_in_table(connect,
                           user_id,
                           assistant,
                           response)
        
