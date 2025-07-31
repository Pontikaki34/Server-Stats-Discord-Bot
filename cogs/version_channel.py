import discord
from discord.ext import commands, tasks
import aiohttp

GITHUB_RELEASE_API = "https://api.github.com/repos/yourusername/yourrepo/releases/latest"

class VersionChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.version = "1.0.0"  # default starting version
        self.update_version.start()

    def cog_unload(self):
        self.update_version.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.ensure_channel(guild)

    @tasks.loop(minutes=30)
    async def update_version(self):
        new_version = await self.fetch_github_version()
        if new_version and new_version != self.version:
            self.version = new_version
            for guild in self.bot.guilds:
                await self.update_channel(guild)

    async def fetch_github_version(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(GITHUB_RELEASE_API) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("tag_name", None)
            except Exception:
                return None

    async def ensure_channel(self, guild: discord.Guild):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            category = await guild.create_category("Server Stats")

        channel_name = f"Version {self.version}"

        channel = discord.utils.get(category.channels, name__startswith="Version")
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

        channel_name = f"Version {self.version}"

        channel = discord.utils.get(category.channels, name__startswith="Version")
        if channel:
            await channel.edit(name=channel_name)

async def setup(bot):
    await bot.add_cog(VersionChannel(bot))
