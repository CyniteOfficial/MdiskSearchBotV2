from TeamTeleRoid.database import db
from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.types import Message

VERIFY = {}
@Client.on_message(filters.command("add_api") & filters.group)
async def group_hanler(c: Client, m: Message):
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

    if len(m.command) == 1:
        return await m.reply('Command Usage: /add_api your api key')
    if not await db.get_group(chat_id):
        return await m.reply('Group is not added by the owner')
    if len(m.command) == 2:
        api=m.command[1]
        if await db.get_api_id(chat_id):
            await db.update_user_api(group_id=m.chat.id, api=api)
            return await m.reply('API ID Updated successfully')
        else:
            await db.add_user_api(group_id=m.chat.id, api=api)
            return await m.reply('API ID added successfully')
