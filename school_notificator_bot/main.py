import asyncio, discord, json, os

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

@slash.slash(name="register_channel", description="알림을 전송할 채널을 등록합니다", options=[create_option(name="channel", description="전송할 채널", option_type=7, required=True)])
async def run(message, channel: str):
    with open("channels.json", 'r', encoding='UTF-8') as f:
        channels = dict(json.load(f))
    channels["channels"].append(channel.id)
    with open("channels.json", 'w', encoding='UTF-8') as f:
        json.dump(channels, f)
    await message.send("채널 등록이 완료되었습니다")

@client.event
async def on_ready():
    print('봇시작')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="학교 정보")) #상태설정
    discord.Permissions.use_slash_commands = True

client.run(token)