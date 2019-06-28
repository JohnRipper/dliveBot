import logging
from lib.message import Message
class Cog:

    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot


    async def chatdelete(self, data):
        self.logger.info(f'ChatDelete: {data}')


    async def message(self, data):
        self.logger.info(f'Message: {data}')
        message = Message(self.bot, data)
        for p in self.bot.settings['global_prefixes']:
            if message.content.startswith(p):
                command, msg = message.content[len(p):].split(" ", 1)
                await self.on_command(command, msg)

    async def chatmoderator(self, data: dict):
        #someone was madea  chat moderator
        return None

    async def on_command(self, command: str, message: str):
        return None