import asyncio, discord

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

@slash.slash(name="register_channel", description="알림을 전송할 채널을 등록합니다", options=[create_option(name="command", description="실행 할 명령", option_type=3, required=True)])
async def run(message, command: str):
    if message.channel.id == 968088658093690920:
        result = subprocess.check_output(command, shell=True).decode('ascii')
        print(result)
        if len(result) > 2000:
            await message.send(result[0:2000])
            await message.send("메시지가 너무 길어 2000자만 보냅니다.")
        else:
            await message.send(result)
    else:
        await message.send("서버 관리 채널에서만 사용할 수 있는 명령어입니다.")

@client.event
async def on_ready():
    print('봇시작')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="학교 정보")) #상태설정
    discord.Permissions.use_slash_commands = True

client.run(token)