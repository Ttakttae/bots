import asyncio, discord, random, time, pickle, threading, subprocess
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option


# 변수
player = 0
player_Info = {}
card_game = {'wait' : {}, 'start' : {}}
# 'start' : {'room_name' : {'game_money' : 0, 'players' : [player1_name, player2_name], 'cards' : [player1_card, player2_card]}}
# 'wait' : {'room_name' : {'game_money' : 0, 'players' : [player1_name, player2_name]}}

bok_card = {}
# bok_card = {'복권 번호' : [[True/False, 가격], [True/False, 가격], [True/False, 가격], [True/False, 가격]]}

# 플레이어 정보 가져오기
with open("player_Info", 'rb') as fr:
    player_Info = pickle.load(fr)

master_id = ['']


#토큰
token = ''
print("Token_key : ", token)

#설정
intents = discord.Intents.default()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)

#시작
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/명령어"))
    print("=============START=============")

@slash.slash(name="정보", description="내 정보를 확인합니다")
async def info(message):
    if not str(message.author.id) in player_Info:
        player_Info[str(message.author.id)] = {'money' : 0, 'game' : ""}
        player_Info[str(message.author.id)]['money'] += 20000

    if player_Info[str(message.author.id)]['money'] <= 0:
        embed = discord.Embed(title="내 정보", description="파산하셨습니다. 관리자에게 돈 지급을 요청하세요.", color=0xacf6f1)
        await message.send(embed=embed)
    else:
        embed = discord.Embed(title="내 정보", description="돈 : {0}".format(player_Info[str(message.author.id)]['money']), color=0xacf6f1)
        await message.send(embed=embed)

    with open("player_Info", 'wb') as fw:
        pickle.dump(player_Info, fw)

@slash.slash(name="지급", description="돈을 지급합니다", options=[create_option(name="people", description="지급할 사람", option_type=3, required=True), create_option(name="amount", description="지급할 돈의 액수", option_type=4, required=True)])
async def give_money(message, people: str, amount: int):
    if not str(message.author.id) in player_Info:
        player_Info[str(message.author.id)] = {'money' : 0, 'game' : ""}
        player_Info[str(message.author.id)]['money'] += 20000
    if str(message.author.id) in master_id:
        name = people
        if "!" in name:
            name_id = name[3:-1]
        else:
            name_id = name[2:-1]

        player_Info[name_id]['money'] += amount
        await message.send(content="지급완료")

    with open("player_Info", 'wb') as fw:
        pickle.dump(player_Info, fw)

@slash.slash(name="복권", description="복권을 뽑습니다")
async def lottery(message):
    if not str(message.author.id) in player_Info:
        player_Info[str(message.author.id)] = {'money' : 0, 'game' : ""}
        player_Info[str(message.author.id)]['money'] += 20000
    if player_Info[str(message.author.id)]['money'] < 4000:
        await message.send(content="돈이 없습니다[<@%s>]" % (str(message.author.id)))
        return None
    player_Info[str(message.author.id)]['money'] -= 4000
    rand_n = random.randint(1, 100)
    if rand_n <= 60: # 60%
        n = 2000
    elif rand_n <= 88: # 28%
        n = 5000
    elif rand_n <= 98: # 10%
        n = 8000
    elif rand_n <= 100: # 2%
        n = 20000

    while True:
        bok_id = random.randint(1000,9999)
        if not bok_id in bok_card:
            break

    icons = ['🧡', '❌', '🍕', '🚓', '🎈', '🎄', '🥽', '⚽', '🏳', '🌎']
    icon = []
    while len(icon) != 4:
        choice_icon = random.choice(icons)
        if not choice_icon in icon:
            icon.append(choice_icon)


    msg = await message.send(content="준비중...")

    await msg.add_reaction("✅")
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    await msg.add_reaction("4️⃣")

    bok_card[bok_id] = [msg, n, {1:"⬜⬜",2:"⬜⬜",3:"⬜⬜",4:"⬜⬜"}, str(message.author.id), icon]
    embed = discord.Embed(title="복권 - %s" % (str(message.author)), description="⬜⬜ | 2000원\n⬜⬜ | 5000원\n⬜⬜ | 8000원\n⬜⬜ | 20000원", color=0xacf6f1)
    embed.set_footer(text="1️⃣2️⃣3️⃣4️⃣ : 열기, ✅ : 보상 받기")
    await msg.edit(content = "B0-%i-%s" % (bok_id, str(message.author.id)),embed = embed)

    with open("player_Info", 'wb') as fw:
        pickle.dump(player_Info, fw)

@slash.slash(name="카드", description="카드 게임을 합니다", options=[create_option(name="command", description="명령(참가, 나가기, 교체, 돈추가)", option_type=3, required=True), create_option(name="room", description="참가/나가기할 방", option_type=3, required=False), create_option(name="amount", description="배팅할 돈의 액수/추가할 돈의 액수", option_type=3, required=False)])
async def card(message, command: str, room: str, amount: str):
    if not str(message.author.id) in player_Info:
        player_Info[str(message.author.id)] = {'money' : 0, 'game' : ""}
        player_Info[str(message.author.id)]['money'] += 20000
    if command == "참가":
        if room in card_game['wait']:
            card_game['start'][room] = {'game_money' : card_game['wait'][room]['game_money'] + amount, 'players' : [card_game['wait'][room]['players'][0], str(message.author.id)], 'cards' : []}
            del card_game['wait'][room]
            embed = discord.Embed(title="카드", description="방 이름 : ***{0}***\n인원 : ***2***/2\n걸린 돈 : ***{1}G***".format(room, card_game['start'][room]['game_money']), color=0xacf6f1)
            await message.send(content="카드 {0}".format(room),embed=embed)
            player_Info[str(message.author.id)]['game'] = ["card", room]
            await message.send(content="게임 시작")
        else:
            card_game['wait'][room] = {'game_money' : amount, 'players' : [str(message.author.id)]}
            embed = discord.Embed(title="카드", description="방 이름 : ***{0}***\n인원 : ***1***/2\n걸린 돈 : ***{1}G***".format(room, card_game['wait'][room]['game_money']), color=0xacf6f1)
            await message.send(content="카드 {0}".format(room), embed=embed)
            player_Info[str(message.author.id)]['game'] = ["card", room]

    elif command == "나가기" and player_Info[str(message.author.id)]['game'][0] == "card":
        if not player_Info[str(message.author.id)]['game'] == "":
            del card_game['wait'][player_Info[str(message.author.id)]['game'][1]]
            player_Info[str(message.author.id)]['game'] = ""
            await message.send(content="방에서 나가짐")

    with open("player_Info", 'wb') as fw:
        pickle.dump(player_Info, fw)

#@client.event
#async def on_message(message):
#    if message.author.bot:
#        return None
#
#    if message.content.startswith(';'):
#
#        if not str(message.author.id) in player_Info:
#            player_Info[str(message.author.id)] = {'money' : 0, 'game' : ""}
#            player_Info[str(message.author.id)]['money'] += 20000
#
#        #잡다한 관리자 권한
#        #if str(message.author.id) in master_id:
#            #player_Info[str(message.author.id)]['money'] = 20000
#
#        content = message.content[1:]
#        commend_word = []
#        start = 0
#        for n in range(len(content)):
#            if content[n:n+1] == " ":
#                commend_word.append(content[start:n])
#                start = n + 1
#            if n + 1 == len(content):
#                commend_word.append(content[start:])
#
#        # await message.channel.send(commend_word) 테스트용
#
#        if commend_word[0] == "도움" or commend_word[0] == "ㄷㅇ" or commend_word[0] == "help":
#            if len(commend_word) >= 2:
#                if commend_word[1] == "정보" or commend_word[1] == "ㅈㅂ" or commend_word[1] == "info":
#                    embed = discord.Embed(title="명령어 사용법", description=";***정보***", color=0x57ff1a)
#                    await message.channel.send(embed=embed)
#
##                if commend_word[1] == "지급" or commend_word[1] == "ㅈㄱ" or commend_word[1] == "lend":
##                    embed = discord.Embed(title="명령어 사용법", description="대출하기\n ;대츨\n 빚 갚기\n ;빚갚기", color=0x57ff1a)
##                    await message.channel.send(embed=embed)
#
#                if commend_word[1] == "카드" or commend_word[1] == "ㅋㄷ" or commend_word[1] == "card":
#                    embed = discord.Embed(title="명령어 사용법", description="`> 게임 참가 및 나가기`\n;***카드 참가 [방이름] [돈]***\n;***카드 나가기 [방이름]***\n\n`> 게임 플레이`\n;***카드 교체***\n;***카드 돈추가 [돈]***", color=0x57ff1a)
#                    await message.channel.send(embed=embed)
#
#                if commend_word[1] == "도움" or commend_word[1] == "ㄷㅇ" or commend_word[1] == "help":
#                    embed = discord.Embed(title="명령어 사용법", description=";***도움 [명령어]***", color=0x57ff1a)
#                    await message.channel.send(embed=embed)
#                if commend_word[1] == "복권" or commend_word[1] == "ㅂㄱ" or commend_word[1] == "lotto":
#                    embed = discord.Embed(title="명령어 사용법", description=";***도움***", color=0x57ff1a)
#                    await message.channel.send(embed=embed)
#            else:
#                embed = discord.Embed(title="도움말", description="`> 기본`\n***도움 [명령어]*** : 명령어 사용법을 봅니다\n***정보*** : 나의 정보를 봅니다\n\n`> 게임`\n***카드*** : 상대 카드만 보고 상대 카드보다 숫자가 높으면 이기는 게임입니다\n(보상 : 판돈 2배)\n***복권*** : 4000에 복권을 구매해 사용합니다\n(보상 : 2000, 4000, 10000, 100000 중에서 1개)", color=0x57ff1a)
#                await message.channel.send(embed=embed)
#
#        # 내정보
#        if commend_word[0] == "정보" or commend_word[0] == "ㅈㅂ" or commend_word[0] == "info":
#            if player_Info[str(message.author.id)]['money'] <= 0:
#                embed = discord.Embed(title="내 정보", description="파산하셨습니다. 관리자에게 돈 지급을 요청하세요.", color=0xacf6f1)
#                await message.channel.send(embed=embed)
#            else:
#                embed = discord.Embed(title="내 정보", description="돈 : {0}".format(player_Info[str(message.author.id)]['money']), color=0xacf6f1)
#                await message.channel.send(embed=embed)
#
#        if commend_word[0] == "지급" and str(message.author.id) in master_id:
#            name = commend_word[1]
#            if "!" in name:
#                name_id = name[3:-1]
#            else:
#                name_id = name[2:-1]
#
#            player_Info[name_id]['money'] += int(commend_word[2])
#            await message.channel.send("지급완료")
#
##        #잡다한 관리자 권한
##        if commend_word[0] == "초기화" or commend_word[0] == "ㅊㄱㅎ" or commend_word[0] == "reset" and str(message.author.id) in master_id:
##            with open("player_Info", 'wb') as fw:
##                pickle.dump(player_Info, fw)
##            dls =subprocess.check_output(["python3", "reset_player_Info.py"])
##            with open("player_Info", 'rb') as fr:
##                player_Info = pickle.load(fr)
##            await message.channel.send("성공적으로 사용자 데이터 초기화를 완료하였습니다.")
###           if "@" in commend_word[1]:           #여기서 특정 사용자의 데이터를 초기화하고 싶은데 할줄 모르겠음 ㅋㅋㅋㅋㅋㅋ
###               player_Info[str(message.author.id)]['money'] == 20000
###               player_Info[str(message.author.id)]['lend_money'] += 0
###       if commend_word[0] == "종료" or commend_word[0] == "shutdown": #ㅈㄹ로 안한 이유 : 채팅하다 ㅈㄹ ㅈㄹ 많이 말해서ㅋㅋㅋㅋㅋ   #여기서 break해서 정상 종료 되는지 의문.........
###           with open("player_Info", 'wb') as fw:
###               pickle.dump(player_Info, fw)
###           dls =subprocess.check_output(["git", "add", "player_Info"])
###           dls =subprocess.check_output(["git", "commit", "-m", "player_info_save"])
###           dls =subprocess.check_output(["git", "push", "origin", "main"])
###           break
##        if commend_word[0] == "업데이트" or commend_word[0] == "ㅇㄷㅇㅌ" or commend_word[0] == "update" and str(message.author.id) in master_id:
##            dls =subprocess.check_output(["git", "pull", "origin", "main"])
##            await message.channel.send("성공적으로 업데이트를 완료하였습니다. 업데이트를 적용하기 위해서는 프로그램을 종료 후 다시 실행시켜주세요.")
##        if commend_word[0] == "정보저장" or commend_word[0] == "ㅈㅂㅈㅈ" or commend_word == "save" and str(message.author.id) in master_id:
##            with open("player_Info", 'wb') as fw:
##                pickle.dump(player_Info, fw)
##            dls =subprocess.check_output(["git", "add", "player_Info"])
##            dls =subprocess.check_output(["git", "commit", "-m", "player_info_save"])
##            dls =subprocess.check_output(["git", "push", "origin", "main"])
##            await message.channel.send("서버에 사용자 정보를 성공적으로 저장하였습니다.")
##
#
#        # 카드게임 BETA
#        if commend_word[0] == "카드" or commend_word[0] == "card":
#            if commend_word[1] == "참가" or commend_word[1] == "join":
#                if commend_word[2] in card_game['wait']:
#                    card_game['start'][commend_word[2]] = {'game_money' : card_game['wait'][commend_word[2]]['game_money'] + int(commend_word[3]), 'players' : [card_game['wait'][commend_word[2]]['players'][0], str(message.author.id)], 'cards' : []}
#                    del card_game['wait'][commend_word[2]]
#                    embed = discord.Embed(title="카드", description="방 이름 : ***{0}***\n인원 : ***2***/2\n걸린 돈 : ***{1}G***".format(commend_word[2], card_game['start'][commend_word[2]]['game_money']), color=0xacf6f1)
#                    await message.channel.send("카드 {0}".format(commend_word[2]),embed=embed)
#                    player_Info[str(message.author.id)]['game'] = ["card", commend_word[2]]
#                    await message.channel.send("게임 시작")
#                else:
#                    card_game['wait'][commend_word[2]] = {'game_money' : int(commend_word[3]), 'players' : [str(message.author.id)]}
#                    embed = discord.Embed(title="카드", description="방 이름 : ***{0}***\n인원 : ***1***/2\n걸린 돈 : ***{1}G***".format(commend_word[2], card_game['wait'][commend_word[2]]['game_money']), color=0xacf6f1)
#                    await message.channel.send("카드 {0}".format(commend_word[2]), embed=embed)
#                    player_Info[str(message.author.id)]['game'] = ["card", commend_word[2]]
#
#            elif commend_word[1] == "나가기" and player_Info[str(message.author.id)]['game'][0] == "card":
#                if not player_Info[str(message.author.id)]['game'] == "":
#                    del card_game['wait'][player_Info[str(message.author.id)]['game'][1]]
#                    player_Info[str(message.author.id)]['game'] = ""
#                    await message.channel.send("방에서 나가짐")
#
#        if commend_word[0] == "복권" or commend_word[0] == "ㅂㄱ" or commend_word[0] == "lotto":
#            if player_Info[str(message.author.id)]['money'] < 4000:
#                await message.channel.send("돈이 없습니다[<@%s>]" % (str(message.author.id)))
#                return None
#            player_Info[str(message.author.id)]['money'] -= 4000
#            rand_n = random.randint(1, 100)
#            if rand_n <= 60: # 60%
#                n = 2000
#            elif rand_n <= 88: # 28%
#                n = 5000
#            elif rand_n <= 98: # 10%
#                n = 8000
#            elif rand_n <= 100: # 2%
#                n = 20000
#
#
#            while True:
#                bok_id = random.randint(1000,9999)
#                if not bok_id in bok_card:
#                    break
#
#            icons = ['🧡', '❌', '🍕', '🚓', '🎈', '🎄', '🥽', '⚽', '🏳', '🌎']
#            icon = []
#            while len(icon) != 4:
#                choice_icon = random.choice(icons)
#                if not choice_icon in icon:
#                    icon.append(choice_icon)
#
#
#            msg = await message.channel.send("준비중...")
#
#            await msg.add_reaction("✅")
#            await msg.add_reaction("1️⃣")
#            await msg.add_reaction("2️⃣")
#            await msg.add_reaction("3️⃣")
#            await msg.add_reaction("4️⃣")
#
#            bok_card[bok_id] = [msg, n, {1:"⬜⬜",2:"⬜⬜",3:"⬜⬜",4:"⬜⬜"}, str(message.author.id), icon]
#            embed = discord.Embed(title="복권 - %s" % (str(message.author)), description="⬜⬜ | 2000원\n⬜⬜ | 5000원\n⬜⬜ | 8000원\n⬜⬜ | 20000원", color=0xacf6f1)
#            embed.set_footer(text="1️⃣2️⃣3️⃣4️⃣ : 열기, ✅ : 보상 받기")
#            await msg.edit(content = "B0-%i-%s" % (bok_id, message.author.id),embed = embed)
#
#
#
#
#    print("{0}/{1}/{2}({4}) : {3}".format(message.guild.name,message.channel.name,message.author.name,str(message.content), message.author.id))
#
#    with open("player_Info", 'wb') as fw:
#        pickle.dump(player_Info, fw)


# 리엑션 버튼
@client.event
async def on_reaction_add(reaction, user):
    if user.bot == 1:
        return None

    
    if reaction.message.content[:2] == "B0":
        bok_id = int(reaction.message.content[3:7])
        player_id = str(reaction.message.content[8:])

        if player_id != str(user.id):
            return None

        icon = bok_card[bok_id][4]

        n = bok_card[bok_id][1]
        choice = 0
        gold = 0

        if reaction.emoji == "1️⃣":
            choice = 1
            gold = 2000
        if reaction.emoji == "2️⃣":
            choice = 2
            gold = 5000
        if reaction.emoji == "3️⃣":
            choice = 3
            gold = 8000
        if reaction.emoji == "4️⃣":
            choice = 4
            gold = 20000
        
        if reaction.emoji == "✅":
            embed = discord.Embed(title="복권", description="***%i 원***" % n, color=0xacf6f1)
            await bok_card[bok_id][0].edit(content = "",embed = embed)
            player_Info[bok_card[bok_id][3]]['money'] += n
            del bok_card[bok_id]
            return None


        if gold == n:
            bok_card[bok_id][2][choice] = "%s%s" % (icon[choice-1], icon[choice-1])
        else:
            first_icon = icon[choice - 1]
            while True:
                second_icon = random.choice(icon)
                if second_icon != first_icon:
                    break

            bok_card[bok_id][2][choice] = "%s%s" % (first_icon, second_icon)

        embed = discord.Embed(title="복권 - %s" % (str(user)), description="{0} | 2000원\n{1} | 5000원\n{2} | 8000원\n{3} | 20000원".format(bok_card[bok_id][2][1], bok_card[bok_id][2][2], bok_card[bok_id][2][3], bok_card[bok_id][2][4]), color=0xacf6f1)
        embed.set_footer(text="1️⃣2️⃣3️⃣4️⃣ : 열기, ✅ : 보상 받기")
        await bok_card[bok_id][0].edit(embed = embed)


client.run(token)
