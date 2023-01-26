import discord

targetIDs = []


def is_owner(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator and not any(interaction.user_id == targetIDs):
        return True
    return False


async def SetTargets(ctx, *args):
    global targetIDs
    targetIDs.clear()
    targetIDs.extend(args)
    await ctx.send(f"Set {len(args)} target(s) :thumbsup:")


async def AddTargets(ctx, *args):
    global targetIDs
    targetIDs.extend(args)
    await ctx.send(f"Added {len(args)} target(s) :thumbsup:\nCurrent targets: {len(targetIDs)}")


async def RemoveTargets(ctx, *args):
    global targetIDs
    if len(targetIDs) >= 1:
        deletions = 0
        for i, element in enumerate(targetIDs):
            if any(element == ID for ID in args):
                del targetIDs[i]
                deletions += 1
        if deletions >= 1:
            await ctx.send(f"Removed {deletions} target(s)")
        else:
            await ctx.send("No targets matched your argument(s)")
    else:
        await ctx.send("No current targets :pensive:")


async def ListTargets(ctx):
    if len(targetIDs) >= 1:
        await ctx.send(f"{len(targetIDs)} current targets`\n`{'`, `'.join(targetIDs)}`")
    else:
        await ctx.send("No current targets :pensive:")
