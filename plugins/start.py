from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import User
from utils import texts


@Client.on_message(filters.command(['start']))
async def start(_, msg: Message):
    u = await User.objects.get_or_none(
        user_id=msg.from_user.id
    )
    if u:     
        await msg.reply(texts.START_MESSAGE)
    else:
        await User.objects.create(
            user_id=msg.from_user.id,
            send_time= "18:00",
            number_of_words=5
        )
        await msg.reply(texts.LOGIN_OR_REGISTER,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(texts.LOGIN, "login"), InlineKeyboardButton(texts.REGISTER, "register")]
                    ]
                )
        )
