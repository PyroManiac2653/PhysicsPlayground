import nextcord
from nextcord.ext import commands

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
async def list_channel_overrides(ctx):
    guild = ctx.guild

    response = ""
    for channel in guild.channels:
        response += f"**Channel: {channel.name}**\n"

        # Get the permission overrides for the channel
        overwrites = channel.overwrites
        if not overwrites:
            response += "  No permission overrides.\n"
        else:
            for target, overwrite in overwrites.items():
                response += f"  **{target}**:\n"
                for perm, value in overwrite:
                    response += f"    - {perm}: {'✅' if value is True else '❌' if value is False else '➖'}\n"

        response += "\n"

    # Send the response
    if len(response) > 2000:
        # If the response exceeds Discord's message limit, send it in parts
        for i in range(0, len(response), 2000):
            await ctx.send(response[i:i + 2000])
    else:
        await ctx.send(response)