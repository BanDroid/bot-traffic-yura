__import__("dotenv").load_dotenv()

import discord
from discord.ext import commands
from requests import get
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
    return context.channel.id == "1322836855288234035"


@bot.command(name="total-traffic")
async def total_traffic(context):
    params = {"skipTotal": 1, "sort": "-views", "fields": "id,judul,views"}
    res = get(f"{API_URL}/api/collections/daftar_pj/records", params=params)
    if not res.ok:
        await context.send("Maaf lur, gagal ngambil data traffic, tehe...")
        return
    data = res.json()
    result = "Total traffic semenjak awal data dibuat:\n\n"
    for i, traffic in enumerate(data["items"]):
        result += f"{str(i + 1)}. {traffic['judul']}\nViews: {traffic['views']}\n\n"
    await context.send(result)


bot.run(BOT_TOKEN)
