import datetime
from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db import User
from plugins.start import start
from utils import texts, filters as myfilters
from pytorjoman import Account, errors


@Client.on_callback_query(filters.regex(r'^settings_change_number_of_words_(?P<number>\d{1})$') & myfilters.user_is_registered)
async def change_number_of_words(c, cb: CallbackQuery):
    user = await User.objects.get(user_id=cb.from_user.id)
    try:
        u = await Account.login_from_token(
            c.torjoman,
            user.access_token
        )
    except errors.TokenExpiredError:
        await cb.message.reply(texts.TOKEN_EXPIRED)
        await cb.message.delete()
        user.data['step'] = "main"
        user.access_token = None
        user.refresh_token = None
        await user.update() 
        return
    numow = int(cb.matches[0].group("number"))
    if user.number_of_words != numow:
        user.number_of_words = numow
        await user.update(['number_of_words'])
        await u.update(
            number_of_words=numow
        )
        await cb.answer("Number of words has been updated successfully")
    
    keyboard = [
        [
            InlineKeyboardButton(f"{numow}", f"none")
        ],
        [InlineKeyboardButton(texts.BACK, "settings_change_preferences")]
    ]
    if numow > 0:
        keyboard[0].insert(0, InlineKeyboardButton("➖", f"settings_change_number_of_words_{numow - 1}"))
    if numow < 10:
        keyboard[0].append(InlineKeyboardButton("➕", f"settings_change_number_of_words_{numow + 1}"))        
    await cb.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))

