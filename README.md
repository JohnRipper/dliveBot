# dliveBot

pip install requests, websockets

set your auth key and username of the room you want to join in /data/config.json

run with python bot.py

#Multiple config support
Copy the config and name it something else. then run with python bot.py -c <config_name> 
 
 
 
 #ModuleSupport 
 #AdminModule
 
 reload <module_name>
 
 unload <module_name>
 
 load <module_name>
 
 kys  - quit
 
 
# Making your own modules by overriding on_command or any of the socket events. 


from lib.cog import Cog


class Admin(Cog):
    
    
    async def on_command(command:str, message: str):
        if command == "echo":
            self.bot.send(message)
            
    async def chattext(self, data: dict):
        # You may also work the raw data or convert it into a Message object
        message = Message(self.bot, data)
        print(message.content)
        message.reply("hello world")
        
