from pyrogram import Client , filters
from pyrogram.types import Message, CallbackQuery
from db import User
from utils import texts
from utils.filters import user_step
from pytorjoman import Account, errors
import re
from plugins.start import start

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


@Client.on_callback_query(filters.regex('^register$'))
async def ask_for_first_name(_, cb: CallbackQuery):
    user = await User.objects.get(user_id=cb.from_user.id)
    user.data['step'] = "register_get_first_name"
    await user.update(['data'])
    await cb.edit_message_text(texts.SEND_FIRST_NAME)


@Client.on_message(filters.text & user_step("register_get_first_name") & filters.reply)
async def ask_for_last_name(_, msg: Message):
    if len(msg.text) < 3:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.FIRST_NAME, 3, texts.SEND_FIRST_NAME))
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    user.data = {
        'step': 'register_get_last_name',
        'register': {
            'first_name': msg.text,
        }
    }
    await user.update(['data'])
    await msg.reply_to_message.edit(texts.SEND_LAST_NAME)
    await msg.delete()


@Client.on_message(filters.text & user_step("register_get_last_name") & filters.reply)
async def ask_for_username(_, msg: Message):
    if len(msg.text) < 3:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.LAST_NAME, 3, texts.SEND_LAST_NAME))
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    user.data['step'] = 'register_get_username'
    user.data['register']['last_name'] = msg.text
    await user.update(['data'])
    await msg.reply_to_message.edit(texts.SEND_USERNAME)
    await msg.delete()

@Client.on_message(filters.text & user_step("register_get_username") & filters.reply)
async def ask_for_email(_, msg: Message):
    if len(msg.text) < 5:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.USERNAME, 5, texts.SEND_USERNAME))
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    user.data['step'] = 'register_get_email'
    user.data['register']['username'] = msg.text
    await user.update(['data'])
    await msg.reply_to_message.edit(texts.SEND_EMAIL)
    await msg.delete()

@Client.on_message(filters.text & user_step("register_get_email") & filters.reply)
async def ask_for_password(_, msg: Message):
    if not re.fullmatch(EMAIL_REGEX, msg.text):
        await msg.reply_to_message.edit(texts.INVALID_EMAIL)
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    user.data['step'] = 'register_get_password'
    user.data['register']['email'] = msg.text
    await user.update(['data'])
    await msg.reply_to_message.edit(texts.SEND_PASSWORD_REGISTER)
    await msg.delete()

@Client.on_message(filters.text & user_step("register_get_password") & filters.reply)
async def register(c, msg: Message):
    if len(msg.text) < 8:
        await msg.reply_to_message.edit(texts.FIELD_LENGTH.format(texts.PASSWORD, 5, texts.SEND_PASSWORD_REGISTER))
        await msg.delete()
        return
    user = await User.objects.get(user_id=msg.from_user.id)
    try:
        u = await Account.signup(
            c.torjoman,
            user.data['register']['first_name'],
            user.data['register']['last_name'],
            user.data['register']['email'],
            user.data['register']['username'],
            msg.text,
            "18:00",
            5
        )
    except errors.AlreadyExistError:
        await msg.reply(texts.USER_ALREADY_EXISTS)
        await msg.reply_to_message.delete(); await msg.delete()
        user.data['step'] = "main"
        await user.update(['data']) 
        return await start(c, msg)
    user.data = {
        'step': "main"
    }
    user.access_token = u._access_token
    user.refresh_token = u._refresh_token
    await user.update()
    await msg.reply_to_message.edit(texts.REGISTERED)
    await msg.delete()