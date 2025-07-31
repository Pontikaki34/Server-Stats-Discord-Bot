import discord
from discord.ext import commands

class BotsChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.ensure_channel(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            await self.update_channel(member.guild)

    async def ensure_channel(self, guild: discord.Guild):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            category = await guild.create_category("Server Stats")

        bot_count = sum(1 for m in guild.members if m.bot)
        channel_name = f"Bots: {bot_count}"

        channel = discord.utils.get(category.channels, name__startswith="Bots:")
        if channel is None:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)
            }
            await guild.create_voice_channel(name=channel_name, category=category, overwrites=overwrites)
        else:
            await channel.edit(name=channel_name)

    async def update_channel(self, guild):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            return

        bot_count = sum(1 for m in guild.members if m.bot)
        new_name = f"Bots: {bot_count}"

        channel = discord.utils.get(category.channels, name__startswith="Bots:")
        if channel:
            await channel.edit(name=new_name)

async def setup(bot):
    await bot.add_cog(BotsChannel(bot))
