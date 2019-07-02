import logging
from lib.message import Message
from collections import namedtuple

class Cog:

    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot

    async def chatoffline(self, data: dict):
        return None

    async def chatdelete(self, data: dict):
        return None

    async def chattext(self, data):
        message = Message(self.bot, data)
        for p in self.bot.settings['global_prefixes']:
            if message.content.startswith(p):
                try:
                    data_split = message.content[len(p):].split(" ", 1)
                    command = data_split.pop()
                    msg = ''
                    if data_split:
                        msg = data_split[0]
                    await self.on_command(command, msg)
                except Exception as e:
                    #catch a failed commmand
                    self.logger.debug(e)
                    print(e)
                    await self.bot.send("Something went wrong with this command. contact dev. ")

    async def chatmoderator(self, data: dict):
        # This websocket event is actually a toggle. Look for the Role or a true or false.
        return None

    async def on_command(self, command: str, message: str):
        return None

    async def chattimeout(self, data:dict):
        return None

    async def chatlive(self, data:dict):
        return None