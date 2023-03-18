import datetime
from pyrogram import Client , filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from db import User
from plugins.start import start
from utils import texts, filters as myfilters
from pytorjoman import Account, errors


FIFTEEN_MINUTES = datetime.timedelta(minutes=15)
ONE_HOUR = datetime.timedelta(hours=1)


@Client.on_callback_query(filters.regex(r'^settings_change_sending_time_(?P<time>\d{2}:\d{2}).+$') & myfilters.user_is_registered)
async def change_sending_time(c, cb: CallbackQuery):
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
    time = cb.matches[0].group("time")
    if str(user.send_time) != f"{time}:00":
        user.send_time = time
        await user.update(['send_time'])
        await u.update(
            send_time=time
        )
        await cb.answer("Sending time has been updated successfully")
    before_15_minutes = (datetime.datetime.combine(datetime.date.today(), user.send_time) - FIFTEEN_MINUTES).time()
    before_1_hour = (datetime.datetime.combine(datetime.date.today(), user.send_time) - ONE_HOUR).time()
    after_15_minutes = (datetime.datetime.combine(datetime.date.today(), user.send_time) + FIFTEEN_MINUTES).time()
    after_1_hour = (datetime.datetime.combine(datetime.date.today(), user.send_time) + ONE_HOUR).time()
    
    keyboard = [
        [
            InlineKeyboardButton("➖", f"settings_change_sending_time_{before_15_minutes}"),
            InlineKeyboardButton("➖➖", f"settings_change_sending_time_{before_1_hour}"),
            InlineKeyboardButton("➕➕", f"settings_change_sending_time_{after_1_hour}"),
            InlineKeyboardButton("➕", f"settings_change_sending_time_{after_15_minutes}"),
        ],
        [InlineKeyboardButton(user.send_time.strftime("%I:%M %p"), "none")],
        [InlineKeyboardButton(texts.BACK, "settings_change_preferences")]
    ]
    await cb.edit_message_reply_markup(InlineKeyboardMarkup(keyboard))

