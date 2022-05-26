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
    specification = subprocess.check_output(["neofetch"], shell=True).decode('ascii')[0:2000]
    print(specification)
    await message.send(specification)

@slash.slash(name="run", description="서버의 터미널에 원격으로 명령을 실행시킵니다", options=[create_option(name="command", description="실행 할 명령", option_type=3, required=True)])
async def run(message, command: str):
    if message.channel.id == 968088658093690920:
        commands = command.split(" ")
        result = subprocess.check_output(commands, shell=True).decode('ascii')
        print(result)
        if result > 2000:
            await message.send(result[0:2000])
            await message.send("메시지가 너무 길어 2000자만 보냅니다.")
        else:
            await message.send(result)
    else:
        await message.send("서버 관리 채널에서만 사용할 수 있는 명령어입니다.")

@client.event
async def on_ready():
    print('봇시작')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="서버 관리")) #상태설정
    discord.Permissions.use_slash_commands = True

client.run(token)