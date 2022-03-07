import discord.ext.commands
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

    # @slash_command(guild_ids=[917618398819659866])
    @commands.command()  # TODO: change into a slash command, not working with pycord atm
    async def menu(self, ctx):
        menu_embed = menu.menu_embed(menu.get_menu())
        if isinstance(menu_embed, str):  # Menu failed to get, or no menu
            await ctx.send("Error: Failed to get menu from website")
            return
        await ctx.send(embed=menu_embed)

    @tasks.loop(time=[datetime.time(12)])  # 7AM EST
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
