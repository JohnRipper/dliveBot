from lib.cog import Cog
from lib.message import Message

class Echo(Cog):
    async def streammessagereceived(self, data: dict):
        message = Message(self.bot,data)
        for p in self.bot.settings['global_prefixes']:
            if message.content.startswith(p):
                data_split = str(data['content'])[len(p):].split(" ", 1)
                command = data_split.pop(0)
                if command == "kys":
                    self.bot.disconnect()

                if command == "echo":
                    await self.bot.send(data_split)

