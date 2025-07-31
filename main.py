import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True  # Needed to track member join events

bot = commands.Bot(command_prefix="!", intents=intents)

initial_extensions = [
    "cogs.members_channel",
    "cogs.bots_channel",
    "cogs.roles_channel",
    "cogs.version_channel",
]

async def main():
    async with bot:
        for ext in initial_extensions:
            await bot.load_extension(ext)
        print("Bot is ready and all cogs loaded!")
        await bot.start("YOUR_BOT_TOKEN")  # Replace with your bot token

if __name__ == "__main__":
    asyncio.run(main())
