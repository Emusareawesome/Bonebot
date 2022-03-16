import os

import discord
from discord.ext import commands

import logging
import json

import menu_cog

logging.basicConfig(level=logging.INFO)

# loads config file
if os.path.exists(os.getcwd() + "/config.json"):
    with open(os.getcwd() + "/config.json") as f:
        config_data = json.load(f)
else:
    config_template = {"prefix": "!", "token": ""}  # default template for config file
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(config_template, f)
token = config_data["token"]

description = """Sends updates and prints RHIT menu"""

intents = discord.Intents.default()
# intents.members = True

bot = commands.Bot(command_prefix=config_data["prefix"], description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.add_cog(menu_cog.MenuCog(bot, config_data))

bot.run(token)
