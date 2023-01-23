import random
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
honestlist = []

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="//", intents=discord.Intents.all())

async def on_ready():
    print("Bot has connected to Discord!")


with open("honesty.txt", "r") as honest:
    honestlist = honest.read().split("\n")

@bot.event
async def on_message(message):
    print(message.author.id)
    if message.author.id == 274540674655715330:
        print("triggered")
        index = random.randint(0,len(honestlist))
        await message.channel.send(honestlist[index])

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")



bot.run(TOKEN)