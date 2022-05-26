import asyncio, discord, subprocess, os

from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
from discord_slash.utils.manage_commands import create_option

try:
    load_dotenv("./token.env")
    token = os.getenv('token')
except:
    token = os.environ['token']

print(token)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

@slash.slash(name="specification", description="컴퓨터의 사양을 보여줍니다.")
async def specification(message):
    specification = subprocess.check_output(["neofetch"], shell=True).decode('ascii')
    print(specification)
    await message.send(specification)

client.run(token)