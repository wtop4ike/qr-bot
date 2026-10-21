from io import BytesIO

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, Message
from qrcode.exceptions import DataOverflowError

from config import DEFAULT_LANGUAGE
from translations import translate
from utils import generate_qr, read_qr

router = Router()


def tr(message: Message, key: str) -> str:
    return translate(key, getattr(message.from_user, "language_code", None) or DEFAULT_LANGUAGE)


@router.message(Command("start"))
async def start_message(message: Message) -> None:
    await message.answer(tr(message, "start"))


@router.message(F.photo | F.document)
async def decode(message: Message, bot: Bot) -> None:
    image = message.photo[-1] if message.photo else message.document
    if image.file_size and image.file_size > 10 * 1024 * 1024:
        await message.answer(tr(message, "too_large"))
        return
    buffer = BytesIO()
    try:
        await bot.download(image, destination=buffer)
    except TelegramAPIError:
        await message.answer(tr(message, "download_error"))
        return
    text = await read_qr(buffer.getvalue())
    if text is None:
        await message.answer(tr(message, "not_found"))
    elif not text:
        await message.answer(tr(message, "empty"))
    else:
        for start in range(0, len(text), 2000):
            await message.answer(text[start:start + 2000], parse_mode=None)


@router.message(F.text)
async def encode(message: Message) -> None:
    try:
        image = await generate_qr(message.text)
    except DataOverflowError:
        await message.answer(tr(message, "text_too_large"))
        return
    await message.answer_document(BufferedInputFile(image, filename="qr.png"))


@router.message()
async def unsupported(message: Message) -> None:
    await message.answer(tr(message, "unsupported"))
