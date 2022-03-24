import os

import discord
from discord.ext import commands

import logging
import json

import menu_cog
import quotes_cog

logging.basicConfig(level=logging.INFO)

# loads config file
if os.path.exists(os.getcwd() + "/config.json"):
    with open(os.getcwd() + "/config.json") as f:
        config_data = json.load(f)
else:
    config_template = {"prefix": "!", "token": "", "menuChannels": [], "randomFooterMessages": True,
                       "footerMessages": [], "quotesChannel": 0}  # default template for config file
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(config_template, f)
token = config_data["token"]

description = """Sends updates and prints RHIT menu"""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config_data["prefix"], description=description, intents=intents)
tree = bot.tree



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.add_cog(menu_cog.MenuCog(bot, config_data))
    await bot.add_cog(quotes_cog.QuotesCog(bot, config_data))
    await tree.sync(guild=discord.Object(id=917618398819659866))


bot.run(token)
