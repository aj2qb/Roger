import apscheduler
import asyncio
import datetime 

from datetime import datetime       # DON'T get rid of this import, sends user format error
from discord import Member 
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import UserInputError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from typing import Optional 

class eventRemind(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def sendReminder(self, member: Member, *, message: str):
        await member.send(f"{message}")
        # print(f"Member: {member} Message: {message}")

    @command(name="rogerRemind", aliases=["RogerRemind", "remindMe", "RemindMe", "remindme"])
    async def rogerRemind(self, ctx, date: str, time: str, amPM: str):
        amPM = amPM.upper()
        dateList = []
        dateList = date.split("/")
        timeList = []
        timeList = time.split(":")

        if(amPM != "AM" and amPM != "PM"):
            await ctx.send(f"{ctx.author.mention} Format error. Use '$rogerFormat for help.")
            return  

        # Datetime uses 24 hours... users in discord do not
        if(amPM == "PM"):
            if int(timeList[0]) == 12: 
                timeList[0] = int(timeList[0])
            else: 
                timeList[0] = int(timeList[0])
                timeList[0] += 12

        # Ensures date and time is properly formatted 
        try: 
            notify = datetime.datetime(int(dateList[2]), int(dateList[0]), int(dateList[1]), 
                                         int(timeList[0]),  int(timeList[1]), 0)
        except: 
            await ctx.send(f"{ctx.author.mention} Format error. Please ensure: \n 1. All needed information is given \n 2. Valid date & time is given \n You can use '$rogerFormat' for help.")
            return  

        realMsg="No message to remind you."
        if ctx.message.reference is not None:
            msg = await ctx.fetch_message(ctx.message.reference.message_id)
            realMsg = msg.content
        else: 
            await ctx.send(f"{ctx.author.mention} {realMsg}")
            return 
          
        # print(f"Remind me when it is: {notify}")
        scheduleMessage = AsyncIOScheduler()
        scheduleMessage.add_job(eventRemind.sendReminder, "date", args=[self, ctx.author], kwargs={"message":f"{realMsg}"}, run_date=notify)
        scheduleMessage.start()

    @rogerRemind.error
    async def roger_Remind_Error(self, ctx, exc): 
        if(isinstance(exc, UserInputError)): 
            await ctx.send(f"{ctx.author.mention} Format error. AM/PM not specified. You can use '$rogerFormat' for help.")


    @command(name="rogerFormat", aliases=["format", "Format", "RogerFormat", "rogerformat"])
    async def rogerFormat(self, ctx): 
        await ctx.send("$rogerRemind XX/XX/XXXX XX:XX AM/PM")

    @command(name="formatEvent", aliases=["formatevent", "FormatEvent", "rogerFormatEvent", "RogerFormatEvent", "rogerformatevent"])
    async def rogerFormatEvent(self, ctx):
        pass

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("eventRemind") # this function tells the bot that the cog is ready
            # pass in the name of the file there not the class


def setup(bot):
    bot.add_cog(eventRemind(bot))