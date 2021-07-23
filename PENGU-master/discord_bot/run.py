import asyncio, discord, os, pickle, random, time, subprocess
from discord.ext import commands

###########################################
last_update = {'ED' : ['챗봇 기능 삭제', '로또 코드 임시 삭제'], 'HP' : [], 'F' : "False", 'ER': [], 'EVT' : []}
ver = "v1.91+ED"
"""다음 버전: 예외 줄이기//릴레이 소설 앨범만들기//GUI UPDATE"""
op_name = ['Pio', 'Windows 10', 'Codedis'] #최고 관리자
###########################################
event = False





with open("bad_list.txt","rb") as fr: #읽기
    bad_list = pickle.load(fr)
with open("text_everyone.txt","rb") as fr: #읽기
    everyone_list = pickle.load(fr)
with open("lolling.txt","rb") as fr: #읽기
    lolling_list = pickle.load(fr)


global_chet = {'list':[]}


#토큰
token = ''
print("Token_key : ", token)

go = True

#설정
game = discord.Game('펭구 도움')
bot = commands.Bot(command_prefix="펭구 ", status=discord.Status.online,activity=game, help_command=None)
client = discord.Client()

#시작
@bot.event
async def on_ready():
    print("봇 시작")
    with open("log.txt","a") as fw:
        fw.write("\n-----------------")

@bot.event
async def on_member_join(member):
    return None
    # 대충 환영메시지
    # await member.send("")

@bot.event
async def on_guild_join(guild):
    await guild.create_role(name="펭구 관리자")

@bot.event
async def on_message(message):
    global go, ver, last_update, op_name, lolling_list, page # lotto_list, event, player_info, item_info,``
    try:
        if not message.guild.id in bad_list:
            bad_list[message.guild.id] = []
    except:
        print("개인/{0} : {1}".format(message.author.name, str(message.content)))
        f = open("log.txt",'a', encoding="utf-8")
        f.write("\n[{0}]개인/{1} : {2}".format(str(time.strftime('%Y-%m-%d-%H-%M-%S')), message.author.name, str(message.content)))
        f.close()
        if str(message.content) == "펭구베타":
            channel = await message.author.create_dm()
            embed = discord.Embed(title="베타 테스트", description="[참여하기](<%s>)" % 'https://discord.gg/UyPZdp5wj4', color=0x62c1cc)
            msg = await message.channel.send(embed=embed)
        elif str(message.content) == "펭구코드":
            channel = await message.author.create_dm()
            embed = discord.Embed(title="펭구 코드", description="펭구 코드 [보러가기](<%s>)" % 'https://github.com/heyyouhub/PENGU_VER', color=0x62c1cc)
            await message.channel.send(embed=embed)
        return None #그냥 무시(나중에 개발하자)
    f = open("log.txt",'a', encoding="utf-8")
    f.write("\n[{0}]{1}/{2}/{3} : {4}".format(str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))),str(message.guild.name),str(message.channel.name),str(message.author.name),str(message.content)))
    f.close()
    if go == False and message.content.startswith(':켜기') and message.author.name in op_name:
        embed = discord.Embed(title="켜기", description="봇 켬", color=0x62c1cc)
        await message.channel.send(embed=embed)
        go = True
            
    if message.author.bot or go == False: #만약 메시지를 보낸사람이 봇일 경우에는
        return None #동작하지 않고 무시합니다.
    try:
        if global_chet[str(message.channel.id)]:
            for i in range(len(global_chet['list'])):
                if not global_chet['list'][i][1] == message.channel:
                    channel_id = global_chet['list'][i][1]
                    await channel_id.send("{0} : {1}".format(str(message.author.name), str(message.content)))
    except: pass


    message_content = message.content
    for txt in bad_list[message.guild.id]:
        bad = message_content.find(txt)
        if bad >= 0:
            if message.author.bot:
                embed = discord.Embed(title="", description=":bangbang: 봇한테 욕 시키지 마세요~\n ||대상:<@{0}> 부르기: @펭구 관리자 ||".format(message.author.id), color=0x62c1cc)
                delete_msg = await message.channel.send(embed=embed)
                await message.delete()
            else:
                # embed = discord.Embed(title="", description=":bangbang: 욕설을 하시면 경고를 받습니당~\n ||대상:<@{0}> 부르기: @펭구 관리자 ||".format(message.author.id), color=0x62c1cc)
                # delete_msg = await message.channel.send(embed=embed)
                await message.delete()
        await bot.process_commands(message)
    print("{0}/{1}/{2} : {3}".format(message.guild.name,message.channel.name,message.author.name,str(message.content)))
    #펭구야 삭제

    if message.content.startswith('펭구야'):
        await message.channel.send('?')

    elif message.content.startswith(':데려오기'):
        embed = discord.Embed(title="데려오는 중!!", description="[데려가는 곳](<%s>)" % 'https://discord.com/api/oauth2/authorize?client_id=757397292390154271&permissions=8&scope=bot', color=0x62c1cc)#-------------------------------------------------------------
        embed.set_footer(text="주의 사항!! : '펭구 관리자' 역할이 새로 생깁니다!")#-------------------------------------------------------------
        await message.channel.send(embed=embed)

    elif message.content.startswith('펭구 도움'):
        page = ['```:버전```\n```:데려오기```', '게임\n```:소설 [보기/쓰기]```', '관리자 명령어\n```:지우기 [개수]```\n```:욕설리스트```\n```:욕설[추가/삭제] [욕설]```\n```공지기능 : ⤴️을 메시지 보내고 달으면 됩니다```']
        embed = discord.Embed(title=":scroll: 도움(명령어!)", description=page[0], color=0x62c1cc)
        embed.set_footer(text="◀️:이전장 ▶️:다음장 ❌:끄기")
        msg = await message.channel.send("페이지[0]", embed=embed)
        await msg.add_reaction('▶️')
        await msg.add_reaction('❌')
    
    elif message.content.startswith(':홍보하기'):
        embed = discord.Embed(title="울랄라시", description="https://discord.gg/bQup75a\n게임방입니다..", color=0x62c1cc)
        await message.channel.send(embed=embed)
        

    elif message.content.startswith(':버전'):
        find = ['ED', 'HP', 'ER', 'EVT']
        result = {}
        for i in range(len(find)):
            result[find[i]] = ""
            if len(last_update[find[i]]) > 0:
                for n in range(len(last_update[find[i]])):
                    result[find[i]] += "{0}.{1}\n".format(n+1, last_update[find[i]][n])
            else:
                result[find[i]] = ":x: \n"
        embed = discord.Embed(title="PENGU[:%s]" % ver, description="이벤트:joystick: \n{0}\n에러:no_entry: \n{1}\n픽스:wrench: \n{2}\n추가:inbox_tray: \n{3}".format(result['EVT'], result['ER'], result['HP'], result['ED']), color=0x62c1cc)
        embed.set_thumbnail(url="https://upload2.inven.co.kr/upload/2019/11/17/bbs/i15270280003.jpg")
        embed.set_footer(text="Full_version : {0}".format(last_update['F']))
        await message.channel.send(embed=embed)

    elif message.content.startswith(':소설 '):
        txt = message.content[4:6]
        if txt == "보기":
            result = ""
            for line in lolling_list:
                result += line + "\n"
            embed = discord.Embed(title="릴레이 소설", description=result, color=0x62c1cc)
            await message.channel.send(embed=embed)
        elif txt == "쓰기":
            txt = str(message.content[6:])
            if txt == "":
                embed = discord.Embed(title="릴레이 소설", description="소설의 내용을 적어주세요", color=0x62c1cc)
                await message.channel.send(embed=embed)
            lolling_list.append(str(len(lolling_list) + 1) + ". " + txt + "[%s]" % (str(message.author.name)))
            with open("lolling.txt","wb") as fw:
                pickle.dump(lolling_list, fw)
            embed = discord.Embed(title="릴레이 소설", description="소설의 새 줄을 썼습니다", color=0x62c1cc)
            await message.channel.send(embed=embed)
        
        elif txt == "폭파" and str(message.author.name) in op_name:
            embed = discord.Embed(title="릴레이 소설", description="암살 성공", color=0x62c1cc)
            await message.channel.send(embed=embed)
            lolling_list = []
            with open("lolling.txt","wb") as fw:
                pickle.dump(lolling_list, fw)


    for i in range(len(message.author.roles)):
        if message.author.roles[i].name == '펭구 관리자' or message.author.name in op_name:

            if message.content.startswith(':욕설추가 '):
                bad_list[message.guild.id].append(message.content[6:])
                with open("bad_list.txt","wb") as fw:
                    pickle.dump(bad_list, fw)
                await message.delete()
                embed = discord.Embed(title="욕설추가", description="욕설을 새로 추가했습니다", color=0x62c1cc)
                await message.channel.send(embed=embed)
            elif message.content.startswith(':욕설삭제 '):
                bad_list[message.guild.id].remove(message.content[6:])
                with open("bad_list.txt","wb") as fw:
                    pickle.dump(bad_list, fw)
                await delete_msg.delete()
                embed = discord.Embed(title="욕설삭제", description="욕설을 삭제했어요", color=0x62c1cc)
                await message.channel.send(embed=embed)
            elif message.content.startswith(':욕설리스트'):
                result = ""
                for i in bad_list[message.guild.id]:
                    result += str(i) + "\n"
                embed = discord.Embed(title="욕설 리스트", description=result, color=0x62c1cc)
                await message.channel.send(embed=embed)

            elif message.content.startswith(':지우기 '):
                await message.channel.purge(limit=int(message.content[5:]) + 1)
            
            
            elif message.content.startswith(':종료 ') and message.author.name in op_name:
                txt = "v" + str(message.content[4:])
                if ver == txt:
                    embed = discord.Embed(title="종료", description="봇 종료", color=0x62c1cc)
                    embed.set_footer(text="종료 버전: %s" % ver)
                    await message.channel.send(embed=embed)
                    exit()


            elif message.content.startswith(':끄기') and message.author.name in op_name:
                embed = discord.Embed(title="끄기", description="봇 멈춤", color=0x62c1cc)
                await message.channel.send(embed=embed)
                go = False
            
            elif message.content.startswith(':업데이트') and message.author.name in op_name:
                embed = discord.Embed(title="업데이트", description="새로운 버전을 다운로드 중", color=0x62c1cc)
                msg = await message.channel.send(embed=embed)
                subprocess.call('update.bat')
                await msg.delete()
                embed = discord.Embed(title="업데이트", description="적용 및 다시시작", color=0x62c1cc)
                await message.channel.send(embed=embed)
                subprocess.call("restart.bat")
                exit()
            
            elif message.content.startswith(':파일 업로드') and message.author.name in op_name:
                embed = discord.Embed(title="파일 업로드", description="파일 업로드 시작합니다", color=0x62c1cc)
                msg = await message.channel.send(embed=embed)
                go = False
                subprocess.call('file_upload.bat')
                go = True
                await msg.delete()
                embed = discord.Embed(title="파일 업로드", description="파일 업로드 완료", color=0x62c1cc)
                await message.channel.send(embed=embed)
            
            elif message.content == ":챗모드" and message.author.name in op_name:
                print("챗모드 ON")
                channel = message.channel

                while True:
                    txt = str(input("PENGU > "))
                    if txt == "":
                        break
                    await channel.send(txt)
                print("챗모드 OFF")


                
            


                    




@bot.event
async def on_reaction_add(reaction, user):
    global page
    if user.bot == 1: #봇이면 패스
        return None
    if str(reaction.message.content[:3]) == "페이지":
        page_num = int(reaction.message.content[4:5])
        print(page_num)
        if str(reaction.emoji) == "▶️":
            await reaction.message.delete()
            if page_num + 2 >= len(page):
                page_num += 1
                end = True
            else:
                page_num += 1
                end = False
            embed = discord.Embed(title=":scroll: 도움(명령어!)", description=page[page_num], color=0x62c1cc)
            msg = await reaction.message.channel.send("페이지[{0}]".format(page_num),embed=embed)
            await msg.add_reaction('◀️')
            if end == False:
                await msg.add_reaction('▶️')
            await msg.add_reaction('❌')
            
        elif str(reaction.emoji) == "◀️":
            await reaction.message.delete()
            if page_num - 1 <= 0:
                page_num -= 1
                end = True
            else:
                page_num -= 1
                end = False
            embed = discord.Embed(title=":scroll: 도움(명령어!)", description=page[page_num], color=0x62c1cc)
            msg = await reaction.message.channel.send("페이지[{0}]".format(page_num),embed=embed)
            if end == False:
                await msg.add_reaction('◀️')
            await msg.add_reaction('▶️')
            await msg.add_reaction('❌')

        elif str(reaction.emoji) == "❌":
            await reaction.message.delete()


        for i in range(len(reaction.message.author.roles)):
            if reaction.message.author.roles[i].name == '펭구 관리자':
                if str(reaction.emoji) == "⤴️":
                    await reaction.message.delete()
                    embed = discord.Embed(title="", description=str(reaction.message.content), color=0x62c1cc)
                    embed.set_author(name="%s" % (str(reaction.message.author.name)),icon_url=reaction.message.author.avatar_url)
                    await reaction.message.channel.send("@everyone ",embed=embed)



bot.run(token)
