from asyncio import sleep
from datetime import datetime
from discord import Intents
from discord import Embed, File
from glob import glob

from discord.ext.commands import CommandNotFound, BadArgument, UserInputError
from discord.ext.commands import Bot as BotBase
from apscheduler.schedulers.asyncio import AsyncIOScheduler 


PREFIX = "$"
OWNER_IDS = [714338668671664218] # 260226105867239434 ########################################CHANGE THIS
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")] # returns all cogs in the cogs directory

class Ready(object): 
    def __init__(self): 
        for cog in COGS:
            setattr(self, cog, False) # Going through each cog and saying self.cog = false

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'{cog} cog ready')

    def all_ready(self): 
        return all([getattr(self,cog) for cog in COGS]) # checks if all cogs are true


class Bot(BotBase): 
    def __init__(self): 
        self.PREFIX = PREFIX
        self.guild = None
        self.ready = False
        self.cogs_ready = Ready()

        
        super().__init__(
            command_prefix=PREFIX, 
            intents= Intents.all(),
            owner_ids=OWNER_IDS)

    def setup(self):    # this method is what makes the fun cog work
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}') # load_extension makes cog work by accessing the setup(bot) method in fun.py
            print(f'{cog} cog loaded')

        print("Setup complete.")

    def run(self, version): 
        self.Version = version

        print("running setup..")
        self.setup()

        with open("./lib/bot/token", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("running bot") 
        super().run(self.TOKEN, reconnect=True) 

    async def on_connect(self):
        print("bot connected")


    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs): 
        if err == "on_command_error":
            await args[0].send("Something went wrong")

        await self.stdout.send("An error occurred.")
        raise 

    async def on_command_error(self, ctx, exc): 
        if isinstance(exc, CommandNotFound):
            pass
        elif isinstance(exc, BadArgument): 
            pass
        elif hasattr(exc, "original"): # not all errors may have original error attribute
            raise exc.original # raising the original error
        elif isinstance(exc, UserInputError): 
            pass
        else: 
            raise exc

    async def on_ready(self):
        if not self.ready:
           self.guild = self.get_guild(868204577567178753) # 267436776774303746   ########################## UPDATE
           self.stdout = self.get_channel(868204577567178756) # 745811765614608474 ########################## UPDATE
           
           while not self.cogs_ready.all_ready(): # bot won't be ready until all cogs are ready 
               await sleep(0.5)

           self.ready = True
           print("bot is ready")
           # await self.stdout.send("Now online!") 
           
           embed = Embed(title="Hello I'm Roger, nice to meet you! I'm here to help you remember events. Here are the commands I understand:", colour=0x33FFA7, timestamp=datetime.utcnow())
           fields = [("$rogerHelp", "This command will send a list of commands. \n", False),
                  ("$rogerRemind", "This command DMs you reminders for messages you REPLIED to. \n ", False),
                  ("$rogerFormat ", "This command helps you format reminders that you'll use with the '$rogerRemind' command \n", False),
                  ("$rogerFormatEvent", "This command provides a template to detail information for an event. ", False)]

           for name, value, inline in fields: 
                embed.add_field(name=name, value=value, inline=inline)
            
           embed.set_author(name="Roger")
           await self.stdout.send(embed=embed)

        else:
            print("bot reconnected") 


    async def on_message(self, message): 
        if not message.author.bot:  # ignores messages from bots
            await self.process_commands(message)

        else: 
            return 

bot = Bot()


        