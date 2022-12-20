from datetime import datetime
from configs import Config
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from TeamTeleRoid.database import db


@Client.on_message(filters.command("deny_access") & filters.private & filters.chat(Config.BOT_OWNER))
async def dbdeny_access_cmd_handler(c:Client,query: Message):
    print(True)
    try:
        group_id = int(query.command[1])
        user = await db.get_group(str(group_id).replace("-100", ""))
        await db.update_group(str(group_id).replace("-100", ""), {"has_access": False, "last_verified":datetime(2020, 5, 17)})
        await query.reply_text("Group has been banned")
    except Exception as e:
        print(e)


@Client.on_message(filters.command("give_access") & filters.private & filters.chat(Config.BOT_OWNER))
async def give_access_cmd_handler(_, m: Message):
    if len(m.command) == 3:
        group_id = int(m.command[1])
        days = int(m.command[31])
        update = await db.update_group(str(group_id).replace("-100", ""), {
            "has_access": True, 
            "last_verified":datetime.now(),
            "verification_time":days})
        await m.reply_text("Group has been given access")
