import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import date
from days import daily
from months import monthly

load_dotenv()

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_daily(day, month):
    return daily[month-1][day]

def get_monthly(month):
    return monthly[f"{month:02d}"]
 
@bot.event
async def on_ready():
    today = date.today()
    day = today.day
    month = today.month
    print(f"Logged in as {bot.user}!")
    channel = await bot.fetch_channel(CHANNEL_ID)
    if channel:
        await channel.send("## Pranostiky pro dnešní den 🌞☔🌷🍃🌨️📆")
        try:
            lines = get_daily(day, month)
            print("\n".join(lines))
            await channel.send("\n".join(lines))
        except KeyError:
            await channel.send("Na dnešní den nemáme žádnou pranostiku. 😿")
            if random.random() < 0.2:  
                await channel.send("https://floppa.krejzac.cz/floppapi")
            else:
                await channel.send("https://floppa.krejzac.cz/macka")
        if day == 1:
            await channel.send("## Pranostiky pro dnešní měsíc 🗓️😳")
            lines = get_monthly(month)
            await channel.send(get_monthly(month))
    else:
        print("Channel not found.")
    await bot.close() 

bot.run(TOKEN)
