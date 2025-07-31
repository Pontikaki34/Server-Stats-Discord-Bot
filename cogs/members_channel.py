import discord
from discord.ext import commands

class MembersChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.ensure_channel(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            return  # Ignore bots here
        await self.update_channel(member.guild)

    async def ensure_channel(self, guild: discord.Guild):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            category = await guild.create_category("Server Stats")

        member_count = sum(1 for m in guild.members if not m.bot)
        channel_name = f"Members: {member_count}"

        channel = discord.utils.get(category.channels, name__startswith="Members:")
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
            return  # Category missing, ideally create but skip for update

        member_count = sum(1 for m in guild.members if not m.bot)
        new_name = f"Members: {member_count}"

        channel = discord.utils.get(category.channels, name__startswith="Members:")
        if channel:
            await channel.edit(name=new_name)

async def setup(bot):
    await bot.add_cog(MembersChannel(bot))
