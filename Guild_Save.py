import discord
import Target


def save_targets(guild_id, suffix):
    with open(f"{guild_id}_{suffix}","w") as f:
        f.write("\n".join(Target.targetIDs))
        f.close()


def load_targets(guild_id, suffix):
    with open(f"{guild_id}_{suffix}", "r") as f:
        f.write("\n".join(Target.targetIDs))
        f.close()
        
# discord.Guild.id #???? maybe?
# bot.get_guild(id) #????
#ctx er discord's parameters for context information -m
#Jeg begynder at lægge nogle kommentare ind i bot.py