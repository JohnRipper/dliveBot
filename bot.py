import os
import json
import sys
import getopt
import logging
import websockets
import asyncio
import time
import concurrent.futures
import importlib
import requests
from lib.message import Message
from lib import constants
__author__ = "John Ripper"
__version__ = "0.2"
name = "Ramblr"

logging.basicConfig(filename='logs/debug',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


class Bot:

    def __init__(self):
        self.logger = logging.getLogger('bot')
        self.ws = None
        self.connected = False
        self.interval = 0
        self.s = None
        self.is_running = True
        self.settings = None
        self.cogs = []
        self.username = ''
        self.role = ''
        self.message_queue = []
        self.rate_limit_seconds = 1

    def load_config(self, config=None):
        if config is None:
            config = 'config'
        with open(f'./data/config/{config}.json') as data_file:
            self.settings = json.load(data_file)
        self.load_cogs()

    async def connect(self):
        async with websockets.connect(uri='wss://graphigostream.prd.dlive.tv/',
                                      subprotocols=['graphql-ws'],
                                      extra_headers=constants.get_headers(self.settings['auth_key']),
                                      ) as self.ws:
            self.connected = True
            await self.ws.send(json.dumps(constants.get_init_payload()))
            print('running')
            await self.ws.send(json.dumps(constants.get_StreamMessageSubscription(self.settings["room"])))
            async for message in self.ws:
                await self.consumer(message)

    def add_cog(self, cog_name: str):
        try:
            m = importlib.import_module(f'modules.{cog_name.lower()}')
            cog_class = getattr(m, cog_name)
            cog = cog_class(bot=self)
            self.cogs.append(cog)
            return True
        except Exception as e:
            print(e)

    def remove_cog(self, cog_name: str):
        for cog in self.cogs:
            if cog.name == cog_name:
                self.cogs.remove(cog)
                return True

    def load_cogs(self):
        for cog_name in self.settings['modules']:
            self.add_cog(cog_name)

    async def consumer(self, message: str):
        print(message)
        d_crap = json.loads(message)
        self.logger.info(message)
        # TODO map out all socket events.
        if d_crap['type'] == "data":
            for data_type in constants.T_OBJECTS:
                if data_type in d_crap['payload']['data']:
                    if data_type is constants.STREAMMESSAGERECEIVED:
                        # why is this even a list? ehh figure it out later
                        for object in d_crap['payload']['data']['streamMessageReceived']:
                            for type in constants.STREAM_T_OBJECTS:
                                # this cog code only runs hen a stream message type is detected. wonder wht other types do.
                                for cog in self.cogs:
                                    await getattr(cog, type.lower())(object)

    async def send(self, message: str):
        self.message_queue.append(message)


    def disconnect(self):
        self.is_running = False
        self.ws.close()

    def process_message_queue(self):
        while self.is_running:
            if len(self.message_queue) > 0:
                print(self.settings['room'])
                time.sleep(self.rate_limit_seconds)
                headers = {
                    'authorization': self.settings['auth_key'],
                    'content-type': 'application/json', 'Origin': 'https://dlive.tv', 'Referer': 'https://dlive.tv/'}
                # todo set the correct streamer room/username.
                data = {"operationName": "SendStreamChatMessage", "variables": {
                    "input": {"streamer": self.settings['room'], "message": self.message_queue.pop(0), "roomRole": "Owner",
                              "subscribing": True}},
                        "extensions": {"persistedQuery": {"version": 1,
                                                          "sha256Hash": "e755f412252005c7d7865084170b9ec13547e9951a1296f7dfe92d377e760b30"}}}
                r = requests.post(url='https://graphigo.prd.dlive.tv/',
                                  headers=headers,
                                  data=json.dumps(data))
                self.logger.info(r.text)
                time.sleep(self.rate_limit_seconds)

def process_arg(arg, b: Bot):
    try:
        opts, args = getopt.getopt(arg, "c:s:", ["config=", "create="])
    except getopt.GetoptError:
        print('Bot.py -c <configfile>')
        sys.exit(2)
    # load default config if one is not specified.
    if not opts:
        b.load_config()

    for opt, arg in opts:
        if opt == '-c':
            b.load_config(arg)
        if opt == '-s':
            if not os.path.isfile(f'./data/config/{arg}.json'):
                print("specified config does not exist. ")
                print("creating config. ")
                with open('./data/config.json', 'w', ) as outfile:
                    json.dump({u"auth_key": None,
                               }, outfile, indent=4)
                print(f"check and correct /data/config/{arg}.json")
                sys.exit()


async def start(executor, b: Bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.process_message_queue),
    await b.connect()


if __name__ == "__main__":
    bot = Bot()
    try:
        process_arg(sys.argv[1:], bot)
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1, )
        asyncio.get_event_loop().run_until_complete(start(executor, bot))
    except Exception as e:
        print(e.__str__())
        bot.disconnect()
