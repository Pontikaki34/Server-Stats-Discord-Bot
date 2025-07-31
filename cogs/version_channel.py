import discord
from discord.ext import commands, tasks
import aiohttp

# Replace with your repo info
GITHUB_VERSION_FILE_URL = "https://raw.githubusercontent.com/Pontikaki34/Server-Stats-Discord-Bot/main/version.txt"

class VersionChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.local_version = "1.0.0"  
        self.update_version.start()

    def cog_unload(self):
        self.update_version.cancel()

    async def fetch_github_version(self):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(GITHUB_VERSION_FILE_URL) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        return text.strip()
            except Exception:
                return None

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            await self.ensure_channel(guild)

    @tasks.loop(minutes=30)
    async def update_version(self):
        github_version = await self.fetch_github_version()
        if github_version:
            for guild in self.bot.guilds:
                await self.update_channel(guild, github_version)

    async def ensure_channel(self, guild: discord.Guild):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            category = await guild.create_category("Server Stats")

        github_version = await self.fetch_github_version()

        if github_version == self.local_version:
            channel_name = "Version Up To Date"
        else:
            channel_name = "Version Not Up To Date"

        channel = discord.utils.get(category.channels, name__startswith="Version")
        if channel is None:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)
            }
            await guild.create_voice_channel(name=channel_name, category=category, overwrites=overwrites)
        else:
            await channel.edit(name=channel_name)

    async def update_channel(self, guild, github_version):
        category = discord.utils.get(guild.categories, name="Server Stats")
        if category is None:
            return

        if github_version == self.local_version:
            channel_name = "Version Up To Date"
        else:
            channel_name = "Version Not Up To Date"

        channel = discord.utils.get(category.channels, name__startswith="Version")
        if channel:
            await channel.edit(name=channel_name)

async def setup(bot):
    await bot.add_cog(VersionChannel(bot))
