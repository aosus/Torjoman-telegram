from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db import User
from plugins.start import start
from utils import texts, filters as myfilters
from pytorjoman import Account, errors


@Client.on_callback_query(filters.regex('^settings_change_preferences$'))
async def change_preferences_main(_, cb: CallbackQuery):
    user = await User.objects.get(user_id=cb.from_user.id)
    user.data['step'] = "main"
    await user.update(['data'])
    await cb.edit_message_reply_markup(InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(texts.FIRST_NAME, "settings_change_first_name")],
            [InlineKeyboardButton(texts.LAST_NAME, "settings_change_last_name")],
            [InlineKeyboardButton(texts.SENDING_TIME, f"settings_change_sending_time_{user.send_time}")],
            [InlineKeyboardButton(texts.NUMBER_OF_WORDS, f"settings_change_number_of_words_{user.number_of_words}")],
        ]
    ))

