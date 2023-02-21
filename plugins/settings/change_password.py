from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db import User
from plugins.start import start
from utils import texts, filters as myfilters
from pytorjoman import Account, errors


@Client.on_callback_query(filters.regex('^settings_change_password$'))
async def ask_for_old_password(_, cb: CallbackQuery):
    user = await User.objects.get(user_id=cb.from_user.id)
    user.data['step'] = "settings_get_old_password"
    await user.update(['data'])
    await cb.edit_message_text(texts.SEND_PASSWORD)

@Client.on_message(filters.text & myfilters.user_step("settings_get_old_password") & filters.reply)
async def ask_for_new_password(_, msg: Message):
    if len(msg.text) < 8:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.PASSWORD, 8, texts.SEND_PASSWORD))
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    user.data = {
        'step': 'settings_get_new_password',
        'change_password': {
            'old_password': msg.text,
        }
    }
    await user.update(['data'])
    await msg.reply_to_message.edit(texts.SEND_NEW_PASSWORD)
    await msg.delete()


@Client.on_message(filters.text & myfilters.user_step("settings_get_new_password") & filters.reply)
async def change_password(c, msg: Message):
    if len(msg.text) < 8:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.PASSWORD, 5, texts.SEND_NEW_PASSWORD))
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
    try:
        await u.change_password(
            user.data['change_password']['old_password'],
            msg.text
        )
    except errors.IncorrectPasswordError:
        await msg.reply(texts.INCORRECT_PASSWORD)
        await msg.reply_to_message.delete(); await msg.delete()
        user.data['step'] = "settings_get_old_password"
        await user.update(['data'])
        return
    user.access_token = u._access_token
    user.refresh_token = u._refresh_token
    user.data = {
        'step': "main"
    }
    await user.update()
    await msg.reply_to_message.edit(texts.PASSWORD_CHANGED)
    await msg.delete()
