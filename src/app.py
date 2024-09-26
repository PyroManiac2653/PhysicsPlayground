import os

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

import typing
from typing import Optional

intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# @bot.event
# async def on_ready():
#     print(f"Bot is ready. Logged in as {bot.user}")

# @bot.slash_command(name="hello", description="Says hello!")
# async def hello(interaction: Interaction):
#     await interaction.response.send_message("Hello, world!")

@bot.slash_command(name="online-test", description="Provides a status if bot is online.")
async def testE(interaction: Interaction):
    s = f" (Guild: {interaction.guild_id})" if interaction.guild_id is not None else ""
    await interaction.response.send_message(f"Bot is online!{s}", ephemeral=True)

@bot.slash_command(name="option-test2", description="Option test description.")
async def echo_number(
    interaction: Interaction, number: str = SlashOption(required=True)):
    await interaction.response.send_message(f"You said: {number}")

async def on_message(message):
    
    # Check if the message is a DM
    if message.guild is None and not message.author.bot:
        user = message.author
        print(f"DM from: {user.name} (ID: {user.id})")
        
        await message.channel.send(f"Hello, {user.name}! I received your DM.")

    # Process commands if using commands in the bot
    await bot.process_commands(message)

# Run the bot with the token
token = os.environ['DISCORD_PHYSICS_PLAYGROUND_BOT_TOKEN']
bot.run(token)