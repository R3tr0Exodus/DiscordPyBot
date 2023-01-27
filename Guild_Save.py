import discord
import Target

fileExt = ".targets"
path = "saves/"


def save_targets(guild_id, suffix):
    with open(f"{path}{guild_id}_{suffix}{fileExt}", "w") as f:
        f.write("\n".join(Target.targetIDs[guild_id]))
        f.close()


def load_targets(guild_id, suffix):
    with open(f"{path}{guild_id}_{suffix}{fileExt}", "r") as f:
        Target.targetIDs[guild_id] = f.read().replace(" ", "").split("\n")
        f.close()
        
