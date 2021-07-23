import asyncio, discord, os, pickle, random, time, subprocess
from discord.ext import commands



#토큰
token = ''
print("Token_key : ", token)

#설정
game = discord.Game('안내')
bot = commands.Bot(command_prefix=";;:", status=discord.Status.online,activity=game, help_command=None)
client = discord.Client()

#시작
@bot.event
async def on_ready():
    print("=============START=============")


@bot.event
async def on_message(message):
    # 봇 감지 제외
    if message.author.bot:
        return None
    
    if message.content == '' or message.content == '':
        await message.channel.send(" 는 아직 개발중이에요. 조금만 더 기다리시면 재미있는 끝말잇기 게임을 즐기실 수 있으니 기대해주세요!")
        
    print(message.content)

bot.run(token)
