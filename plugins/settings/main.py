from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import User
from utils import texts, filters as myfilters
from pytorjoman import Account, errors

@Client.on_message(filters.command(['settings']) & myfilters.user_is_registered)
async def main_menu(c, msg: Message):
    user = await User.objects.get_or_none(
        user_id=msg.from_user.id
    )
    u = await Account.login_from_token(c.torjoman, user.access_token)
    await msg.reply(texts.SETTINGS_MAIN, reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(texts.CHANGE_PREFERENCES, "settings_change_preferences")],
            [InlineKeyboardButton(texts.CHANGE_PASSWORD, "settings_change_password")]
        ]
    )
    )
