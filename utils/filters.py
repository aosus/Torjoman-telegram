from pyrogram import filters
from db import User

def user_step(step: str):
    async def func(flt, _, update):
        return (await User.objects.get(user_id=update.from_user.id)).data['step'] == flt.step

    return filters.create(func, step=step)