import discord
import Target

fileExt = ".targets"
path = "saves/"


def save_targets(guild_id, suffix):
    with open(f"{path}{guild_id}_{suffix}{fileExt}", "w") as f:
        f.write("\n".join(Target.targetIDs))
        f.close()


def load_targets(guild_id, suffix):
    with open(f"{path}{guild_id}_{suffix}{fileExt}", "r") as f:
        Target.targetIDs = f.read().replace(" ", "").split("\n")
        f.close()
        
# discord.Guild.id #???? maybe?
# bot.get_guild(id) #????
#ctx er discord's parameters for context information -m
#Jeg begynder at lægge nogle kommentare ind i bot.py