from pyrogram import Client, filters
import datetime
from configs import Config
from TeamTeleRoid.database import db
from pyrogram.types import Message

@Client.on_message(filters.private)
async def handle_user_status(bot:Client, cmd:Message):
    chat_id = cmd.from_user.id

    if not await db.is_user_exist(chat_id):
        print("True")
        await db.add_user(chat_id)
        await bot.send_message(
            Config.LOG_CHANNEL,
            f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
        )

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You Are Ban To Use This Bot.😜", quote=True)
            return
    await cmd.continue_propagation()
