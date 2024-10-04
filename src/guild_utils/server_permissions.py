import nextcord
from nextcord.ext import commands

@bot.command()
async def list_roles(ctx):
    guild = ctx.guild
    roles = guild.roles  # Get all roles in the guild

    # Create a response message with roles and their permissions
    response = "Roles and their permissions:\n\n"
    for role in roles:
        permissions = role.permissions
        response += f"**{role.name}**:\n"
        for perm, value in permissions:
            response += f"  - {perm}: {'✅' if value else '❌'}\n"
        response += "\n"

    # Send the response
    await ctx.send(response)