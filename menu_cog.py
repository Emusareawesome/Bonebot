import discord.ext.commands
from discord import app_commands
from discord.ext import commands, tasks

import datetime

import menu


class MenuCog(commands.Cog):
    def __init__(self, bot: discord.ext.commands.Bot, config_data):
        self.bot = bot
        self.print_menu.start()
        self.config_data = config_data

    def cog_unload(self):
        self.print_menu.cancel()

    @app_commands.command(name="menu", description="Today's menu at the Bon")
    @app_commands.guilds(discord.Object(id=917618398819659866))  # TODO: Comment out when done testing
    async def menu(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True)
        menu_embed = menu.menu_embed(menu.get_menu())
        if isinstance(menu_embed, str):  # Menu failed to get, or no menu
            await interaction.followup.send("Error: Failed to get menu from website")
            return
        await interaction.followup.send(embed=menu_embed)

    @tasks.loop(time=[datetime.time(11)])  # 7AM local, TODO: replace with datetime with timezone
    async def print_menu(self):
        print("sending message")
        menu_embed = menu.menu_embed(menu.get_menu())
        if isinstance(menu_embed, str):  # Menu failed to get, or no menu
            for i in self.config_data["menuChannels"]:
                await self.bot.get_channel(int(i)).send("Error: Failed to get menu from website")
            return
        if type(menu_embed) == discord.Embed:
            for i in self.config_data["menuChannels"]:
                await self.bot.get_channel(int(i)).send(embed=menu_embed)

    @print_menu.before_loop
    async def before_print_menu(self):
        print('waiting...')
        await self.bot.wait_until_ready()
