import re
from configs import Config
import json
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from TeamTeleRoid.database import db
import requests

async def replace_username(text):
	usernames = re.findall("([@#][A-Za-z0-9_]+)", text)
	async for i in AsyncIter(usernames):
		text = text.replace(i, f"@{Config.UPDATES_CHANNEL_USERNAME}")
	return text


#####################  Make link to hyperlink ####################
async def link_to_hyperlink(string):
	http_links = await extract_link(string)
	async for link in AsyncIter(http_links):
		string = string.replace(link, f"[{link}]({link})")
	return string


async def extract_link(string):
	"""
	It takes a string and returns a list of all the URLs in that string
	
	:param string: The string to search for links in
	:return: A list of urls
	"""
	urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
	return urls


import re
async def validate_q(q):
    query = q
            # Checking if the length of the query is less than 2. If it is, it returns.
    if len(query) < 2:
        return False
   
    # Checking if the message contains any of the following:
    #         1. /
    #         2. ,
    #         3. .
    #         4. Emojis
    #         If it does, it will return.
    if re.findall(r"((^\/|^,|^:|^\.|^[\U0001F600-\U000E007F]).*)", query):
        return False
    
    # Checking if the message contains a link.
    if ("https://" or "http://") in query:
        return False

    # It removes the year from the search query.|hello|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|kitt
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|gib)(\sme)?)|new|hd|\(|\)|dedo|print|fulllatest|br((o|u)h?)*um(o)*|aya((um(o)*)?|any(one)|with\ssk)*ubtitle(s)?)", "", query.lower(), flags=re.IGNORECASE)
    return query.strip()





# Converter
async def main_convertor_handler(c:Client, message:Message, type:str, edit_caption:bool=False):
# A function that takes a message and a type and converts the message to the type.
	user_method = type

	METHODS = {
		"mdisk": replace_mdisk_link,
	}
	method_func = METHODS[user_method]

	if message.reply_markup:  # reply markup - button post
		txt = str(message.text)
		reply_markup = json.loads(str(message.reply_markup))
		buttsons = []
		async for i, markup in enumerate(AsyncIter(reply_markup["inline_keyboard"])):
			buttons = []
			async for j in AsyncIter(markup):
				text = j["text"]
				url = j["url"]
				url = await method_func(url)
				regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
				url = re.findall(regex, url)
				button = InlineKeyboardButton(text, url=url[0][0])
				buttons.append(button)
			buttsons.append(buttons)

		txt = await method_func(txt)

		if message.text:
			if edit_caption:
				return await message.edit(txt, reply_markup=InlineKeyboardMarkup(buttsons))

			await message.reply(text=txt, reply_markup=InlineKeyboardMarkup(buttsons))

		elif message.caption:
			if edit_caption:
				return await message.edit_caption(txt, reply_markup=InlineKeyboardMarkup(buttsons))

			if message.photo:
				await message.reply_photo(photo=message.photo.file_id, caption=txt,
											reply_markup=InlineKeyboardMarkup(buttsons))
			elif message.document:
				await message.reply_document(document=message.document.file_id, caption=txt,
												reply_markup=InlineKeyboardMarkup(buttsons))


	elif message.text:
		text = str(message.text)
		if user_method == "droplink" and "|" in text:
			alias = text.split('|')[1].replace(" ", "")
			if len(text) < 30:
				links = re.findall(r'https?://[^\s]+', text)[0]
				link = await method_func(links, alias) 
				await message.reply_text(f"{link}")
				return

		link = await method_func(text)

		if edit_caption:
			return await message.edit(f"{link}")

		await message.reply_text(f"**{link}**")

	elif message.photo:  # for media messages
		fileid = message.photo.file_id
		text = str(message.caption)
		link = await method_func(text)

		if edit_caption:
			return await message.edit_caption(f"{link}")

		await message.reply_photo(fileid, caption=f"{link}")

	elif message.document:  # for document messages
		fileid = message.document.file_id
		text = str(message.caption)
		link = await method_func(text)

		if edit_caption:
			return await message.edit_caption(f"{link}")


		await message.reply_document(fileid, caption=f"{link}")



async def make_bold(string):
	"""
	It takes a string, replaces the first instance of <p> with <p><strong>, and replaces the first
	instance of </p> with </strong></p>
	
	:param string: The string you want to make bold
	:return: The string is being returned with the <p> tags replaced with <p><strong> and </p> replaced
	with </strong></p>
	"""
	string = string.replace("<p>" ,"<p><strong>")
	string = string.replace("</p>" ,"</strong></p>")
	string = string.replace("</h1>" ,"</strong></p>")
	string = string.replace("<h1>" ,"<p><strong>")
	return string


class AsyncIter:    
    def __init__(self, items):    
        self.items = items    

    async def __aiter__(self):    
        for item in self.items:    
            yield item    


# ################################################### Mdisk Convertor #########################################################
        
# async def get_mdisk(link, api=Config.MDISK_API):
async def get_mdisk(link, api=Config.MDISK_API):
	url = 'https://diskuploader.mypowerdisk.com/v1/tp/cp'
	param = {'token': api, 'link': link
			 }
	res = requests.post(url, json=param)
	try:
		shareLink = res.json()
		link = shareLink["sharelink"]
	except:
		pass
	return link

async def replace_mdisk_link(text, api=Config.MDISK_API):
    links = re.findall(r'https?://mdisk.me[^\s]+', text)
    async for link in AsyncIter(links):
        mdisk_link = await get_mdisk(link, api)
        text = text.replace(link, mdisk_link)

    return text


async def group_link_convertor(group_id, text):
    api = await db.get_api_id(group_id)
    if api:
        answer = await replace_mdisk_link(text, str(api['api']))
    else:
        answer = text
    return answer
