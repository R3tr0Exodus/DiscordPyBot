import discord

targetIDs = {}

#           Thorbjørn             Magnus                Atle
invulIDs = ["274540674655715330", "319473108580958208", "266944533042954240"]


def is_owner(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator or any(str(interaction.user.id) == id for id in invulIDs):
        return True #idfk know what im doing, im trynna uck around and find out
    return False


def key_exists(key) -> bool:
    return key in targetIDs and len(targetIDs[key]) >= 1


async def SetTargets(ctx, *args):
    global targetIDs
    targetIDs[ctx.guild.id] = args
    await ctx.send(f"Set {len(args)} target(s) :thumbsup:")


async def AddTargets(ctx, *args):
    global targetIDs
    if key_exists(ctx.guild.id):
        targetIDs[ctx.guild.id].extend(args)
    else:
        targetIDs[ctx.guild.id] = args
    await ctx.send(f"Added {len(args)} target(s) :thumbsup:\nCurrent targets: {len(targetIDs)}")


async def RemoveTargets(ctx, *args):
    global targetIDs
    if key_exists(ctx.guild.id):
        deletions = 0
        for i, element in enumerate(targetIDs[ctx.guild.id]):
            if any(element == ID for ID in args):
                del targetIDs[ctx.guild.id][i]
                deletions += 1
        if deletions >= 1:
            await ctx.send(f"Removed {deletions} target(s)")
        else:
            await ctx.send("No targets matched your argument(s)")
    else:
        await ctx.send("No current targets :pensive:")


async def ListTargets(ctx):
    if key_exists(ctx.guild.id):
        await ctx.send(f"{len(targetIDs[ctx.guild.id])} current targets`\n`{'`, `'.join(targetIDs[ctx.guild.id])}`")
    else:
        await ctx.send("No current targets :pensive:")
