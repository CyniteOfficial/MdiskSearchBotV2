import datetime
from configs import Config
import pymongo


class Database:
    def __init__(self, uri, database_name):
        self._client = pymongo.MongoClient(uri)
        self.db = self._client[database_name]
        self.col = self.db['users']
        self.api_keys = self.db['api_keys']
        self.groups = self.db['groups']
        self.channels = self.db['channels']
        self.grp = self.db.groups

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def add_user(self, id):
        user = self.new_user(id)
        self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = self.col.find_one({'id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users

    async def add_user_api(self, group_id, api):
        api_keys = str(group_id)

        api_keys = api_keys.replace('-100', '')
        api_keys = api_keys.replace('-', '')

        self.api_keys.insert_one(
            {
                'api': api,
                'group_id': int(api_keys)
            }
        )
    
    async def remove_user_api(self, group_id):
        group_id = str(group_id)
        api_keys = group_id.replace('-100', '')
        api_keys = api_keys.replace('-', '')
        api_keys = int(api_keys)

        self.groups.delete_many({'group_id': int(api_keys)})
        self.api_keys.delete_many({'group_id': int(api_keys)})

    async def get_api_id(self, group_id):
        api_keys = str(group_id)
        api_keys = api_keys.replace('-100', '')
        api_keys = api_keys.replace('-', '')
        api = self.api_keys.find_one({'group_id': int(api_keys)})
        return api

    async def get_group(self, group_id):
        group_id = str(group_id)
        group_id = group_id.replace('-100', '')
        group_id = group_id.replace('-', '')

        id = self.groups.find_one({'group_id': int(group_id)})

        if not id:
            res = {
                "group_id": int(group_id),
                "has_access": False,
                "db_channel": 0,
                "last_verified": datetime.datetime(2020, 5, 17),
                "verification_time": Config.VERIFIED_TIME
            }
            self.groups.insert_one(res)

            id = self.groups.find_one({"group_id": group_id})
        return id

    async def update_group(self, group_id, value):
        group_id = int(group_id)
        await self.get_group(group_id)
        myquery = {"group_id": group_id}
        newvalues = { "$set": value }
        self.groups.update_one(myquery, newvalues)

    async def is_group_verified(self, id):
        user = await self.get_group(id)
        try:
            pastDate = user["last_verified"]
        except:
            user = await self.get_group(id)
            pastDate = user["last_verified"]

        if (datetime.datetime.now() - pastDate).days > user["verification_time"] if  user["verification_time"] else Config.VERIFIED_TIME:
            return False
        else:
            return True

    async def update_user_api(self, group_id, api):
        api_keys = str(group_id)

        api_keys = api_keys.replace('-100', '')
        api_keys = api_keys.replace('-', '')

        myquery = {
                'group_id': int(api_keys)
            }
        newvalues = { "$set": {
                'api': api,
                'group_id': int(api_keys)
            } }

        self.api_keys.update_one(myquery, newvalues)

    async def connect(self, group_id,):

        group = str(group_id)

        group = group.replace('-100', '')
        group = group.replace('-', '')
        myquery = {
                'group_id': int(group)
            }

        self.groups.insert_one(myquery)

    async def disconnect(self, group_id,):
        group = str(group_id)

        group = group.replace('-100', '')
        group = group.replace('-', '')
        myquery = {
                'group_id': int(group)
            }
        self.api_keys.delete_many(myquery)
        self.groups.delete_many(myquery)

    async def allow(self, channel_id,):
        channel = str(channel_id)
        channel = channel.replace('-100', '')
        channel = channel.replace('-', '')
        myquery = {
                'status': 'allowed',
                'channel_id': int(channel)
            }
        self.channels.insert_one(myquery)

    async def disallow(self, channel_id,):
        channel = str(channel_id)
        channel = channel.replace('-100', '')
        channel = channel.replace('-', '')
        myquery = {
                'channel_id': int(channel)
            }
        self.channels.delete_many(myquery)


    async def get_channel(self, channel_id,):
        channel = str(channel_id)
        channel = channel.replace('-100', '')
        channel = channel.replace('-', '')
        myquery = {
                'channel_id': int(channel)
            }
        x= self.channels.find_one(myquery)
        if x:return x   

    async def get_channel_count(self):
        channels_count = self.channels.count_documents({"status":"allowed"})
        channels = self.channels.find({"status":"allowed"})
        
        return {
            "count": int(channels_count),
            "channels":channels
        }
    

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)
