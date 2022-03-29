import random

import discord.ext.commands
from discord import app_commands
from discord.ext import commands

import logging


class QuotesCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, config_data):
        self.bot = bot
        self.config_data = config_data
        self.quotes = []

    # @commands.command(name="quote")
    # async def random_quote(self, ctx):
    @app_commands.command(name="quote", description="Random quote from #quotes")
    @app_commands.guilds(discord.Object(id=917618398819659866))  # TODO: remove when done testing
    async def random_quote(self, interaction: discord.Interaction) -> None:
        # TODO: fetch random quote from #quotes channel, maybe make it faster by storing existing quotes within a
        #  json or something idk
        # TODO: append quotes as new messages are made
        if len(self.quotes) == 0:
            await interaction.response.send_message("Error: failed to get quotes")
            return
        quote = random.choice(self.quotes)
        await interaction.response.send_message(quote.content)
        # embed = discord.Embed(title=quote.content, color=0x800000)
        # embed.set_author(name="Original", url=quote.jump_url)
        # await interaction.response.send_message(embed=embed)
        # await ctx.send(embed=embed)

    #  Initialize list of quotes
    async def cog_load(self):
        channel = self.bot.get_channel(self.config_data["quotesChannel"])
        async for message in channel.history():
            if message.content.startswith('"'):
                self.quotes.append(message)
            else:
                logging.log(logging.INFO, message.content)
        logging.log(logging.INFO, "Finished loading quotes")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel != self.bot.get_channel(self.config_data["quotesChannel"]) \
                or message.author.id == self.bot.application_id:
            return
        if message.content.startswith('"'):
            self.quotes.append(message)
            logging.log(logging.INFO, "Added quote")

