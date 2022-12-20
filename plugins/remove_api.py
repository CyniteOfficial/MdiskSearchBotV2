from pyrogram import Client, filters
from pyrogram.types import Message
from TeamTeleRoid.database import db
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

VERIFY = {}

@Client.on_message(filters.command("remove_api") & filters.group)
async def remove_api_handler(c: Client, m: Message):
    global VERIFY
    chat_id = m.chat.id
    user_id = m.from_user.id if m.from_user else None
    if VERIFY.get(str(chat_id)) == None: # Make Admin's ID List
        admin_list = []
        async for x in c.iter_chat_members(chat_id=chat_id, filter="administrators"):
            admin_id = x.user.id 
            admin_list.append(admin_id)
        admin_list.append(None)
        VERIFY[str(chat_id)] = admin_list

    if not user_id in VERIFY.get(str(chat_id)): # Checks if user is admin of the chat
        return

    user_id = m.from_user.id

    if not user_id:
        return await m.reply("Anonymous admin can't remove api")


    api = await db.get_api_id(chat_id)
    if not api:
        return await m.reply("No API found for chat %s" % chat_id)
    reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("Sure !", callback_data=f"remove_api#{chat_id}"),
            InlineKeyboardButton("Cancel", callback_data=f"cancel_removeapi"),]
        ])
    

    return await m.reply('Are you Sure you want to remove your api from this chat?',
    reply_markup=reply_markup)
