from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db import User
from utils import texts, filters as myfilters
from pytorjoman import Account, errors

@Client.on_message(filters.command(['settings']) & myfilters.user_is_registered)
async def main_menu(c, msg: Message):
    await msg.reply(texts.SETTINGS_MAIN, reply_markup=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(texts.CHANGE_PREFERENCES, "settings_change_preferences")],
            [InlineKeyboardButton(texts.CHANGE_PASSWORD, "settings_change_password")]
        ]
    )
    )
