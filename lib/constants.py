
STREAMMESSAGERECEIVED = "streamMessageReceived"
T_OBJECTS = [STREAMMESSAGERECEIVED]

MODERATOR = "Moderator"
DELETE = "Delete"
OFFLINE = "Offline"
TIMEOUT = "Timeout" # MUTE
MESSAGE = "Message"
LIVE = " Live"
STREAM_T_OBJECTS = [MESSAGE, DELETE, MODERATOR, TIMEOUT, LIVE]


CHATMODERATOR = "ChatModerator"
CHATTIMEOUT = "ChatTimeout" # MUTE
CHATDELETE = "ChatDelete"
CHATOFFLINE = "ChatOffline"
CHATTEXT = "ChatText"
CHATLIVE = "ChatLive"
STREAM_TN_OBJECTS = [CHATTEXT, CHATDELETE, CHATTEXT, CHATMODERATOR,CHATTIMEOUT, CHATOFFLINE, CHATLIVE ]



def get_headers(auth_key:str):
    return {"authorization": auth_key,
            "content-type": "application/json",
               "Origin": "https://dlive.tv",
               "Referer": "https://dlive.tv/"}

def get_init_payload():
    return {"type":"connection_init","payload":{}}

def get_StreamMessageSubscription(room: str):
    return {"type":"start","payload":{"variables":{"streamer":room},"operationName":"StreamMessageSubscription","query":"subscription StreamMessageSubscription($streamer:String!){streamMessageReceived(streamer:$streamer){type ... on ChatGift{id gift amount recentCount expireDuration ...VStreamChatSenderInfoFrag}... on ChatHost{id viewer...VStreamChatSenderInfoFrag}... on ChatSubscription{id month...VStreamChatSenderInfoFrag}... on ChatChangeMode{mode}... on ChatText{id content ...VStreamChatSenderInfoFrag}... on ChatFollow{id ...VStreamChatSenderInfoFrag}... on ChatDelete{ids}... on ChatBan{id ...VStreamChatSenderInfoFrag}... on ChatModerator{id ...VStreamChatSenderInfoFrag add}... on ChatEmoteAdd{id ...VStreamChatSenderInfoFrag emote}}}fragment VStreamChatSenderInfoFrag on SenderInfo{subscribing role roomRole sender{id username displayname avatar partnerStatus}}"}}

def get_SendStreamChatMessage(username: str, message: str):
    return {"operationName":"SendStreamChatMessage",
            "variables": {"input":{"streamer":username,"message":message,"roomRole":"Member","subscribing":True},
            "extensions": {"persistedQuery":{"version":1,"sha256Hash":"e755f412252005c7d7865084170b9ec13547e9951a1296f7dfe92d377e760b30"}}}}

#  Generate methods for cog file.
# for o in T_OBJECTS:
#     print(f'async def {o.lower()}(self, data: dict):')
#     print(f'    self.logger.info(f\'{o.lower()}: {{data}}\')')
