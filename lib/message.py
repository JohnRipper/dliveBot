

class Message:
    def __init__(self, bot,  data: dict):
        self.bot = bot
        self.raw = data

        self.message_id = ''
        self.content = ''
        self.sender_id = ''
        self.sender_username = ''
        self.sender_displayname = ''
        self.sender_avatar = ''
        self.sender_displayname = ''
        self.sender_pstatus = ''
        self.sender_role = ''
        self.sender_room_role = ''
        self.subscribing = ''
        # self.badges  its a list but ill do it later
        self.sender_id = ''
        self.load_raw(self.raw)


    def load_raw(self, raw: dict):
        self.message_id = self.raw.get('id','')
        self.content = self.raw.get('content','')
        self.sender_id = self.raw.get('sender','').get('id','')
        self.sender_username = self.raw.get('sender').get('username','')
        self.sender_displayname = self.raw.get('sender','').get('displayname','')
        self.sender_avatar = self.raw.get('sender','').get('avatar','')
        self.sender_displayname = self.raw.get('sender','').get('displayname','')
        self.sender_pstatus = self.raw.get('sender','').get('partnerStatus','')
        self.sender_role = self.raw.get('role','')
        self.sender_room_role = self.raw.get('roomRole','')
        self.subscribing = self.raw.get('subscribing','')
        # self.badges  its a list but ill do it later

    def reply(self, message: str):
        # todo review send statement. create a sendfunction in bot.py
        self.bot.send(message)
