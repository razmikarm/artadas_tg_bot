import json
from aiogram import html
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, access_token: str) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", parse_mode="HTML")


@router.message(Command("help"))
async def help_handler(message: Message, access_token: str):
    await message.answer("This bot responds to /start and /help commands.")


@router.message(Command("whoami"))
async def whoami_handler(message: Message, access_token: str):
    user = message.from_user

    data = dict(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        id=user.id,
        is_bot=user.is_bot,
        language_code=user.language_code,
        jwt_token=access_token,
    )

    await message.answer(json.dumps(data, indent=2))


@router.message()
async def echo_handler(message: Message, access_token: str) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
