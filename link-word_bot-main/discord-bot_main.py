import asyncio, discord, os, pickle, random, time, subprocess
from discord.ext import commands


words = [] # 단어 저장
used_words = [] # 이미 쓴 단어 저장

f = open('word', 'r', encoding='utf-8')
while True:
    data = str(f.readline())
    if not data:
        break
    words.append(data[:-1])
f.close()

#토큰
token = ''
print("Token_key : ", token)

#설정
game = discord.Game('개발')
bot = commands.Bot(command_prefix=";;:", status=discord.Status.online,activity=game, help_command=None)
client = discord.Client()

#시작
@bot.event
async def on_ready():
    print("=============START=============")


@bot.event
async def on_message(message):
    global words, used_words
    # 봇 감지 제외
    if message.author.bot:
        return None
    
    if message.content.startswith('-'):

        player_Input_word = message.content[1:]
        
        if player_Input_word == "새게임":
            used_words.clear()
            await message.channel.send("게임이 초기화 됨")
            return None
        
        if len(player_Input_word) == 1:
            await message.channel.send("한 글자 단어임")
            return None
            
        if player_Input_word == "update":
            dls =subprocess.check_output(["git", "pull", "origin", "main"])
            await message.channel.send("성공적으로 업데이트를 완료하였습니다. 업데이트를 적용하기 위해서는 프로그램을 재시작 해주세요.")
            return None
        
        if player_Input_word in used_words:
            await message.channel.send("이미 쓴 단어")
            return None
        
        used_words.append(player_Input_word)

        if " " in player_Input_word:
            await message.channel.send("단어에 띄어쓰기가 있음")
            return None
        
        # if not player_Input_word in words:
        #     await message.channel.send("사전에 단어가 없음")


        for bot_word in words:
            if bot_word[:1] == player_Input_word[-1:] and not bot_word in used_words:
                used_words.append(bot_word)
                await message.channel.send("{0} -> `{1}`".format(player_Input_word, bot_word))
                return False
        
        await message.channel.send("생각나는 단어가 없음")
        return False

        print(message.content)


bot.run(token)
