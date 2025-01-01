__import__("dotenv").load_dotenv()

import discord
from discord.ext import commands
from requests import get
import aiohttp
from os import environ as env

BOT_TOKEN = env.get("BOT_TOKEN")
BOT_CLIENT_ID = env.get("BOT_CLIENT_ID")
API_URL = env.get("API_URL")

if not BOT_TOKEN or not BOT_CLIENT_ID or not API_URL:
    raise EnvironmentError("BOT_TOKEN, BOT_CLIENT_ID, and API_URL variable is needed!")

description = """Bot YuraManga untuk cek traffic."""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready")


def is_viwers_channel(context):
    return str(context.channel.id) == "1322836855288234035"


@bot.command(name="total-traffic")
async def total_traffic(context):
    if not is_viwers_channel(context):
        await context.reply(
            "Maap lur... gk boleh saya tampilin disini.", mention_author=False
        )
        return
    params = {"skipTotal": 1, "sort": "-views", "fields": "id,judul,views"}
    await context.send("Tunggu bentar yah...", mention_author=False)
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_URL}/api/collections/daftar_pj/records", params=params
        ) as response:
            if not response.ok:
                await context.send("Maaf lur, gagal ngambil data traffic, tehe...")
                return
            data = await response.json()
            result = "Total traffic semenjak awal data dibuat:\n\n"
            for i, traffic in enumerate(data["items"]):
                result += (
                    f"{str(i + 1)}. *{traffic['judul']}*\nViews: {traffic['views']}\n\n"
                )
            await context.reply(result, mention_author=True)
            return


bot.run(BOT_TOKEN)
