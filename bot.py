# Importere forskellige dependencies og libraries bl.a. Discord dotenv og andre
import random
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import Target
import Guild_Save

# Laver et array fra honesty.txt
honestlist = []

# Default cooldown
defaultCooldown = 10
cooldown = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="==", intents=discord.Intents.all())


# Synkronisere botten med oAUTH serveren som bot api'en bliver kørt igennem (Simple Auth? (se docs))
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("With Honesty"))
    print("Bot has connected to Discord!")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} commands")
    except Exception as e:
        print(e)


# Læser of splitter arrayet op i forskellige strings
with open("honesty.txt", "r") as honest:
    honestlist = honest.read().split("\n")
# Sætter prevTime som det tidspunkt en kommando bliver kørt
prevTime = datetime.now()


# Søger om users har et ID der er registreret som Target
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    global prevTime
    if Target.key_exists(message.guild.id):
        if message.guild.id not in cooldown:
            cooldown[message.guild.id] = defaultCooldown
        if (any(int(ID) == message.author.id for ID in Target.targetIDs[message.guild.id])) and (
                datetime.now() >= prevTime + timedelta(seconds=cooldown[message.guild.id])):
            print("triggered")
            index = random.randint(0, len(honestlist) - 1)
            await message.channel.send(honestlist[index])
            prevTime = datetime.now()


# Set cooldown uden / kommandoer
@bot.command()
async def SetCooldown(ctx, arg):
    global cooldown
    if arg.isnumeric():
        cooldown = int(arg)
        await ctx.send(f"Cooldown set to {cooldown} seconds!")
    else:
        await ctx.send(f"{arg} is not a number, smh")


# Sæt targets uden / -- SKAL BRUGE USER-ID --
@bot.command()
async def SetTargets(ctx, *args):
    await Target.SetTargets(ctx, *args)


# Samme som SetTargets man kan have effekt på flere brugere samtidig
@bot.command()
async def AddTargets(ctx, *args):
    await Target.AddTargets(ctx, *args)


# Fjerner Targets -- SKAL BRUGE USER-ID --
@bot.command()
async def RemoveTargets(ctx, *args):
    await Target.RemoveTargets(ctx, *args)


# Sender en liste med alle dem der er registreret som Targets
@bot.command()
async def ListTargets(ctx):
    await Target.ListTargets(ctx)


# Kommando liste men du bruger en / kommando til at se det
@bot.tree.command(name="commands", description="Lists all of honest-bots commands")
async def commands(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(
        f"List of commands:\n\t- SetTargets\n\t- AddTargets\n\t- RemoveTargets\n\t- ListTargets\n\t- SetCooldown",
        ephemeral=True)


# Kommando til at slette hele target listen
@bot.tree.command(name="wipe", description="Wipes all targets that is currently on the Target List")
async def wipe(interaction: discord.Interaction) -> None:
    if Target.key_exists(interaction.guild_id):
        count = len(Target.targetIDs[interaction.guild_id])
        Target.targetIDs[interaction.guild_id].clear()
        await interaction.response.send_message(f"Wiped {count} targets :thumbsup:",
                                                ephemeral=True)
    else:
        await interaction.response.send_message(f"No targets to wipe :pensive:",
                                                ephemeral=True)


# Sæt cooldown med / kommando
@bot.tree.command(name="cooldown", description="Set the cooldown for when the bot")
@app_commands.describe(seconds="Input seconds here here")
async def set_cooldown(interaction: discord.Interaction, seconds: str) -> None:
    if Target.is_owner(interaction):
        global cooldown
        if seconds.isnumeric():
            cooldown[interaction.guild_id] = int(seconds)
            await interaction.response.send_message(f"Cooldown set to {seconds} seconds!",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message(f"{seconds} is not a number, smh",
                                                    ephemeral=True)
    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Sætter et Target for botten -- SKAL BRUGE USER-ID --
@bot.tree.command(name="set_userid", description="Set a user for me to target (Removes all other targets)")
@app_commands.describe(user_id="Input user ID (If multiple ID's separate by comma)")
async def set_user_id(interaction: discord.Interaction, user_id: str) -> None:
    if Target.is_owner(interaction):
        if user_id not in Target.invulIDs:
            user_id_list = user_id.replace(" ", "").split(",")
            Target.targetIDs[interaction.guild_id] = user_id_list
            await interaction.response.send_message(f"Set {len(user_id_list)} target(s) :thumbsup:",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("Sorry, they are too cool to target! :sunglasses:")
    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Add User ID - Samme som Set_User_Id men du kan tilføje mere end en person
@bot.tree.command(name="add_userid", description="Add users for me to target")
@app_commands.describe(user_id="Input user ID (If multiple ID's seperate by comma)")
async def add_user_id(interaction: discord.Interaction, user_id: str) -> None:
    if Target.is_owner(interaction):
        if user_id not in Target.invulIDs:
            user_id_list = user_id.replace(" ", "").split(",")
            if Target.key_exists(interaction.guild_id):
                Target.targetIDs[interaction.guild_id].extend(user_id_list)
            else:
                Target.targetIDs[interaction.guild_id] = user_id_list
            await interaction.response.send_message(
                f"Added {len(user_id_list)} target(s) :thumbsup:\nCurrent targets: {len(Target.targetIDs)}",
                ephemeral=True)
        else:
            await interaction.response.send_message("Sorry, they are too cool to target! :sunglasses:")
    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Fjern Targets (Bruger user id)
@bot.tree.command(name="remove_userid", description="Remove existing targets")
@app_commands.describe(user_id="Input user ID (If you're sending multiple ID's they should be separated by a comma)")
async def remove_user_id(interaction: discord.Interaction, user_id: str) -> None:
    if Target.is_owner(interaction):
        if Target.key_exists(interaction.guild_id):
            user_id_list = user_id.replace(" ", "").split(",")
            deletions = 0
            for i, element in enumerate(Target.targetIDs[interaction.guild_id]):
                if any(int(element) == int(ID) for ID in user_id_list):
                    del Target.targetIDs[interaction.guild_id][i]
                    deletions += 1
            if deletions >= 1:
                await interaction.response.send_message(f"Removed {deletions} target(s)",
                                                        ephemeral=True)
            else:
                await interaction.response.send_message("No targets matched your argument(s)",
                                                        ephemeral=True)
        else:
            await interaction.response.send_message("No current targets :pensive:",
                                                    ephemeral=True)
    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Liste med targets
@bot.tree.command(name="list_targets", description="Lists all of the current targets")
async def list_targets(interaction: discord.Interaction) -> None:
    if Target.is_owner(interaction):
        if Target.key_exists(interaction.guild_id):
            await interaction.response.send_message(
                f"{len(Target.targetIDs[interaction.guild_id])} current targets:\n<@{'>,   <@'.join(Target.targetIDs[interaction.guild_id])}>",
                ephemeral=True)
        else:
            await interaction.response.send_message("No current targets :pensive:",
                                                    ephemeral=True)
    else:
        await interaction.response.send_message("nuh uh! You no Admin!!", ephemeral=True)


# Sender en honest gif/fil
@bot.tree.command(name="honest", description="Sends a random 'My honest opinion' gif")
async def honest(interaction: discord.Interaction) -> None:
    global honestlist
    if interaction.user.id != 417249893938233345:
        index = random.randint(0, len(honestlist) - 1)
        await interaction.response.send_message(honestlist[index])
    else:
        await interaction.response.send_message("Shut the fuck up", ephemeral=True)


# Sætter et target med @'s
@bot.tree.command(name="set_target", description="Set a user for me to target (Removes all other targets)")
@app_commands.describe(user="Input user user")
async def set_targets(interaction: discord.Interaction, user: discord.Member) -> None:
    if Target.is_owner(interaction):
        if str(user.id) not in Target.invulIDs:
            Target.targetIDs[interaction.guild_id] = [str(user.id)]
            await interaction.response.send_message(f"Set 1 target :thumbsup:",
                                                    ephemeral=True)
        else:
            await interaction.response.send_message("Sorry, they are too cool to target! :sunglasses:")
    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Tilføjer flere brugere som targets
@bot.tree.command(name="add_target", description="Adds users to the target list")
@app_commands.describe(user="User")
async def add_target(interaction: discord.Interaction, user: discord.Member) -> None:
    if Target.is_owner(interaction):
        if str(user.id) not in Target.invulIDs:
            if Target.key_exists(interaction.guild_id):
                if any(user.id == int(x) for x in Target.targetIDs[interaction.guild_id]):
                    await interaction.response.send_message("User is already a target!", ephemeral=True)
                Target.targetIDs[interaction.guild_id].extend([str(user.id)])
            else:
                Target.targetIDs[interaction.guild_id] = [str(user.id)]
            await interaction.response.send_message(
                f"Added 1 target :thumbsup:\nCurrent targets: {len(Target.targetIDs[interaction.guild_id])}",
                ephemeral=True)
        else:
            await interaction.response.send_message("Sorry, they are too cool to target! :sunglasses:")

    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Fjerner targets med @'s
@bot.tree.command(name="remove_target", description="Remove existing targets")
@app_commands.describe(user="Input user")
async def remove_target(interaction: discord.Interaction, user: discord.Member) -> None:
    if Target.is_owner(interaction):
        if Target.key_exists(interaction.guild_id):
            deletions = 0
            for i, element in enumerate(Target.targetIDs[interaction.guild_id]):
                if int(element) == user.id:
                    del Target.targetIDs[interaction.guild_id][i]
                    deletions += 1
            if deletions >= 1:
                await interaction.response.send_message(f"Removed {deletions} target(s)",
                                                        ephemeral=True)
            else:
                await interaction.response.send_message("No targets matched your argument(s)",
                                                        ephemeral=True)
        else:
            await interaction.response.send_message("No current targets :pensive:",
                                                    ephemeral=True)
    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Gemmer targets i en seperat fil på botten(?)
@bot.tree.command(name="save_targets", description="Save the current targets")
@app_commands.describe(key="Input a key")
async def save_targets(interaction: discord.Interaction, key: str) -> None:
    if Target.is_owner(interaction):
        Guild_Save.save_targets(interaction.guild_id, key)
        await interaction.response.send_message(f"Saved loadout \"{key}\"", ephemeral=True)

    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


# Loader targets i en separat fil på botten(?)
@bot.tree.command(name="load_targets", description="Load a saved target loadout")
@app_commands.describe(key="Input a key")
async def load_targets(interaction: discord.Interaction, key: str) -> None:
    if Target.is_owner(interaction):
        Guild_Save.load_targets(interaction.guild_id, key)
        await interaction.response.send_message(f"Loaded loadout \"{key}\"", ephemeral=True)

    else:
        await interaction.response.send_message("Nuh uh! You no Admin!!", ephemeral=True)


bot.run(TOKEN)
