import discord
from discord.ext import commands

class RolesChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.ensure_channel(guild)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        await self.update_channel(role.guild)

    async def ensure_channel(self, guild: discord.Guild):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            category = await guild.create_category("Server Stats")

        role_count = len(guild.roles)
        channel_name = f"Roles: {role_count}"

        channel = discord.utils.get(category.channels, name__startswith="Roles:")
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

        role_count = len(guild.roles)
        new_name = f"Roles: {role_count}"

        channel = discord.utils.get(category.channels, name__startswith="Roles:")
        if channel:
            await channel.edit(name=new_name)

async def setup(bot):
    await bot.add_cog(RolesChannel(bot))
