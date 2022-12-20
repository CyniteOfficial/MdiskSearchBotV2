from pyrogram import Client, filters


@Client.on_message(filters.text & filters.incoming & filters.command("id"))
async def id(_, msg):
    await msg.reply(f" Here Is ID : `{msg.chat.id}`", quote=True)
