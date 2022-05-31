import asyncio, discord, json, os, Neis_API
import notificator
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

@slash.slash(name="register_channel_school", description="알림을 전송할 학교와 채널을 등록합니다", options=[create_option(name="channel", description="전송할 채널", option_type=7, required=True), create_option(name="school", description="정보를 전송할 학교의 풀네임(ex.서울고등학교/세화여자고등학교)", option_type=3, required=True)])
async def register_channel_school(message, channel: str, school: str):
    with open("channels.json", 'r', encoding='UTF-8') as f:
        channels = dict(json.load(f))
    if str(channel.id) in channels:
        if school in channels[str(channel.id)]:
            await message.send("이미 등록되어 있는 학교입니다.")
        else:
            channels[str(channel.id)].append(school)
            await message.send("알림을 전송할 학교가 추가되었습니다.")
    else:
        channels[str(channel.id)] = [school]
        await message.send("채널과 학교 등록이 완료되었습니다.")
    with open("channels.json", 'w', encoding='UTF-8') as f:
        json.dump(channels, f)

@slash.slash(name="delete_channel_school", description="알림을 전송할 학교나 채널을 삭제합니다", options=[create_option(name="channel", description="삭제할 채널", option_type=7, required=True), create_option(name="school", description="정보를 전송할 학교의 풀네임(ex.서울고등학교/세화여자고등학교)", option_type=3, required=False)])
async def delete_channel_school(message, channel: str, school: str = None):
    with open("channels.json", 'r', encoding='UTF-8') as f:
        channels = dict(json.load(f))
    if school == None:
        del channels[str(channel.id)]
        await message.send("채널에 대한 알림을 모두 삭제하였습니다.")
    else:
        if school in channels[str(channel.id)]:
            channels[str(channel.id)].remove(school)
            await message.send("해당 채널에서 해당 학교에 대한 정보를 더이상 알림하지 않습니다.")
        else:
            await message.send("해당 채널에서 해당 학교에 대한 알림을 하고 있지 않습니다.")
    with open("channels.json", 'w', encoding='UTF-8') as f:
        json.dump(channels, f)

@slash.slash(name="school_list", description="알림을 받고 있는 학교의 목록을 보여줍니다.", options=[create_option(name="channel", description="전송하는 채널", option_type=7, required=True)])
async def school_list(message, channel: str):
    with open("channels.json", 'r', encoding='UTF-8') as f:
        channels = dict(json.load(f))
    description = ""
    n = 1
    try:
        for a in channels[str(channel.id)]:
            description += f"{n}. {a}\n"
            n += 1
        embed=discord.Embed(title=f"{channel} 채널에서 알림을 전송하고 있는 학교 목록", description=f"{description}")
        await message.send(embed=embed)
    except:
        await message.send("채널에서 전송하고 있는 알림이 한개도 없습니다.")


@client.event
async def on_ready():
    print('봇시작')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="학교 정보")) #상태설정
    discord.Permissions.use_slash_commands = True
    notificator.notificator()


if __name__ == "__main__":
    client.run(token)