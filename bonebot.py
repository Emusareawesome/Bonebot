import os

import discord
import typing
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
    # await tree.sync(guild=discord.Object(id=917618398819659866))

#  !sync ~ for guild sync
@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~"]] = None) -> None:
  if not guilds:
      if spec == "~":
          fmt = await ctx.bot.tree.sync(guild=ctx.guild)
      else:
          fmt = await ctx.bot.tree.sync()

      await ctx.send(
          f"Synced {len(fmt)} commands {'globally' if spec is not None else 'to the current guild.'}"
      )
      return

  assert guilds is not None
  fmt = 0
  for guild in guilds:
      try:
          await ctx.bot.tree.sync(guild=guild)
      except discord.HTTPException:
          pass
      else:
          fmt += 1

  await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")

bot.run(token)
