from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters
from configs import Config
from helpers import *
from TeamTeleRoid.database import db



@Client.on_message(filters.channel & filters.incoming)
async def channel_link_handler(c:Client, m:Message):
    channel_id = m.chat.id
    
    channel_id = await db.get_channel(channel_id)
    if channel_id:
        msg = await m.copy(
            chat_id=Config.CHANNEL_ID,
        )
        try:
            return await main_convertor_handler(c,msg,"mdisk", True)
        except Exception as e:
            print(e)




@Client.on_message(filters.command("allow") & filters.private &  filters.chat(Config.BOT_OWNER))
async def add_channel_handler(_, m: Message):

    if len(m.command) == 1:
        return await m.reply('Command Usage: /allow -100xxx')

    if len(m.command) == 2:
        channel_id=m.command[1]
        if await db.get_channel(channel_id):
            return await m.reply('Channels is already added')
        else:
            await db.allow(channel_id=channel_id,)
            return await m.reply('Channel ID added successfully')



@Client.on_message(filters.command("disallow") & filters.private & filters.chat(Config.BOT_OWNER))
async def remove_channel_handler(c: Client, m: Message):
    if len(m.command) == 1:
        return await m.reply('Command Usage: /disallow -100xxx')

    channel_id=m.command[1]
    channel_id = await db.get_channel(channel_id)
    if not channel_id:
        return await m.reply("No channel found")

    await db.disallow(m.command[1])
    return await m.reply("Channel removed")



@Client.on_message(filters.command("channels") & filters.private & filters.chat(Config.BOT_OWNER))
async def get_channels_list(c: Client, m: Message):
    get_channel = await db.get_channel_count()
    count = get_channel['count']
    channels = get_channel['channels']

    msg = f"""
Total Chats: {count}

Chat List:

"""

    for i, channel in enumerate(channels):
        channel_id = channel['channel_id']
        msg += f"{i+1}) `-100{channel_id}`\n"

    return await m.reply(msg)