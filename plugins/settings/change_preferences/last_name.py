from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db import User
from plugins.start import start
from utils import texts, filters as myfilters
from pytorjoman import Account, errors


@Client.on_callback_query(filters.regex('^settings_change_last_name$'))
async def ask_for_old_last_name(_, cb: CallbackQuery):
    user = await User.objects.get(user_id=cb.from_user.id)
    user.data['step'] = "settings_get_new_last_name"
    await user.update(['data'])
    await cb.edit_message_text(texts.SEND_NEW_LAST_NAME)


@Client.on_message(filters.text & myfilters.user_step("settings_get_new_last_name") & filters.reply)
async def change_last_name(c, msg: Message):
    if len(msg.text) < 3:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.LAST_NAME, 3, texts.SEND_NEW_LAST_NAME))
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    try:
        u = await Account.login_from_token(
            c.torjoman,
            user.access_token
        )
    except errors.TokenExpiredError:
        await msg.reply(texts.TOKEN_EXPIRED)
        await msg.reply_to_message.delete(); await msg.delete()
        user.data['step'] = "main"
        user.access_token = None
        user.refresh_token = None
        await user.update() 
        return await start(c, msg)
    await u.update(
        last_name=msg.text
    )
    user.access_token = u._access_token
    user.refresh_token = u._refresh_token
    user.data = {
        'step': "main"
    }
    await user.update()
    await msg.reply_to_message.edit(texts.LAST_NAME_CHANGED)
    await msg.delete()
