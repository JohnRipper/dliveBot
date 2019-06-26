import logging
from lib.message import Message
class Cog:

    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot

    async def streammessagereceived(self, data: dict):
        self.logger.info(f'hello: {data}')

