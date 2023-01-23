import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
honestlist = []


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="//", intents=discord.Intents.all())

async def on_ready():
    print("Bot has connected to Discord!")


with open("honesty.txt", "r") as honest:
    honestlist = honest.read().split("\n")

prevTime = datetime.now()

@bot.event
async def on_message(message):
    global prevTime
    if message.author.id == 274540674655715330 and datetime.now() >= prevTime + timedelta(0,10):
        print("triggered")
        index = random.randint(0,len(honestlist))
        await message.channel.send(honestlist[index])
        prevTime = datetime.now()



@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")



bot.run(TOKEN)