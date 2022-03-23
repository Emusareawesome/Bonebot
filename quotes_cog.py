import discord.ext.commands
from discord import app_commands
from discord.ext import commands

class QuotesCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    async def random_quote(self, interaction: discord.Interaction) -> None:
        #  TODO: fetch random  quote from #quotes channel, maybe make it faster by storing existing quotes within a json or something idk
        print("placeholder")
