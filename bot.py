import discord
from discord.ext import commands
import random
import os
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
intents.mentions = True

bot = commands.Bot(command_prefix=".", intents=intents)

CAT_RESPONSES = [
    "~nyah~",
    "meow",
    "meow meow! 🐱",
    "purr~ 😺",
    "*stretches* meow~",
]

async def get_cat_image():
    """Fetch a random cat image from cataas.com"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://cataas.com/cat?json=true") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return f"https://cataas.com{data['url']}"
    except Exception:
        pass
    return None


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Meow bot is ready! 🐱")


@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if bot was mentioned
    if bot.user.mentioned_in(message):
        # 70% chance of text response, 30% chance of cat picture
        if random.random() < 0.3:
            cat_url = await get_cat_image()
            if cat_url:
                await message.reply(cat_url)
            else:
                await message.reply(random.choice(CAT_RESPONSES))
        else:
            await message.reply(random.choice(CAT_RESPONSES))

    # Process commands
    await bot.process_commands(message)


@bot.command()
async def meow(ctx):
    """Manual meow command"""
    await ctx.reply(random.choice(CAT_RESPONSES))


@bot.command()
async def catpic(ctx):
    """Get a random cat picture"""
    cat_url = await get_cat_image()
    if cat_url:
        await ctx.reply(cat_url)
    else:
        await ctx.reply("Couldn't fetch a cat pic right now... meow? 🐱")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("ERROR: Please set DISCORD_TOKEN environment variable")
        exit(1)
    bot.run(token)
