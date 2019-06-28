import logging
from lib.message import Message
from lib.cog import Cog


class Admin(Cog):

    async def on_command(self, command: str, message: str):
        if command == "reload":
            await self.reload_module(message)
        if command == "unload":
            await self.unload_module(message)
        if command == "load":
            await self.load(message)
        if command == "kys":
            self.bot.disconnect()

    async def reload_module(self, module: str):
        if await self.unload_module(module):
            await self.load(module)
        await self.bot.send(f"Module: \"{module}\" was reloaded")

    async def unload_module(self, module: str):
        if self.bot.remove_cog(module):
            await self.bot.send(f"Module: \"{module}\" was unloaded")
        else:
            await self.bot.send(f"Module: \"{module}\" was not found. unable to unload.")

    async def load(self, module: str):
        if self.bot.add_cog(module):
            await self.bot.send(f"Module: \"{module}\" was loaded")
        else: 
            await self.bot.send(f"Module: \"{module}\" failed to load")

