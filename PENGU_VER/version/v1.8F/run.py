import asyncio, discord, os, pickle, random, time, subprocess
from discord.ext import commands

###########################################
# ED 추가적인 기능이나 코드
# HP 핫픽스
# F 풀버전
last_update = "FULL_VER : 릴레이소설기록오류"
ver = "v1.8F+ED"
"""다음 버전: 예외 줄이기//릴레이 소설 앨범만들기"""
op_name = ['Pio', 'Windows 10'] #최고 관리자
###########################################


with open("bad_list.txt","rb") as fr: #읽기
    bad_list = pickle.load(fr)
with open("study.txt","rb") as fr: #읽기
    study = pickle.load(fr)
with open("text_everyone.txt","rb") as fr: #읽기
    everyone_list = pickle.load(fr)
with open("lolling.txt","rb") as fr: #읽기
    lolling_list = pickle.load(fr)


global_chet = {'list':[]}


#토큰
token_path = os.path.dirname(os.path.abspath(__file__)) + "/token.txt"
t = open(token_path, "r", encoding="utf-8")
token = t.read().split()[0]
print("Token_key : ", token)

go = True

#설정
game = discord.Game('펭구 도움[%s]' % ver)
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
    return
    #await member.send("")

@bot.event
async def on_guild_join(guild):
    await guild.create_role(name="펭구 관리자")

@bot.event
async def on_message(message):
    global go, ver, last_update, op_name
    try:
        if not message.guild.id in bad_list:
            bad_list[message.guild.id] = []
    except:
        print("개인/{0} : {1}".format(message.author.name, str(message.content)))
        f = open("log.txt",'a', encoding="utf-8")
        f.write("\n[{0}]개인/{1} : {2}".format(str(time.strftime('%Y-%m-%d-%H-%M-%S'), message.author.name, str(message.content))))
        f.close()
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
                embed = discord.Embed(title="", description="봇한테 욕 시키지 마세요~\n ||대상:<@{0}> 부르기: @펭구 관리자 ||".format(message.author.id), color=0x62c1cc)
                delete_msg = await message.channel.send(embed=embed)
                await message.delete()
            else:
                embed = discord.Embed(title="", description="욕설을 하시면 경고를 받습니당~\n ||대상:<@{0}> 부르기: @펭구 관리자 ||".format(message.author.id), color=0x62c1cc)
                delete_msg = await message.channel.send(embed=embed)
                await message.delete()
        await bot.process_commands(message)
    print("{0}/{1}/{2} : {3}".format(message.guild.name,message.channel.name,message.author.name,str(message.content)))

    if message.content.startswith('펭구야 '):
        if message.content[4:] in study:
            await message.channel.send(study[message.content[4:]][random.randint(0, len(study[message.content[4:]]) -1)])
        else:
            await message.channel.send('?')
    elif message.content.startswith(':가르치기 '):
        for i in range(len(message.content)):
            if message.content[i] == ";":
                if not message.content[6:i] in study:
                    study[message.content[6:i]] = []
                    study[message.content[6:i]].append(message.content[i+1:])
                else:
                    study[message.content[6:i]].append(message.content[i+1:])
        with open("study.txt","wb") as fw:
            pickle.dump(study, fw)
        embed = discord.Embed(title="가르치기", description="새로운 것을 배웠어요", color=0x62c1cc)
        await message.channel.send(embed=embed)
    elif message.content.startswith(':잊어버려 '):
        for i in range(len(message.content)):
            if message.content[i] == ";":
                if message.content[6:i] in study:
                    study[message.content[6:i]].remove(message.content[i+1:])
                    if len(study[message.content[6:i]]) == 0:
                        del study[message.content[6:i]]
        with open("study.txt","wb") as fw:
            pickle.dump(study, fw)
        embed = discord.Embed(title="잊어버려", description="배운 것을 잊었어요", color=0x62c1cc)
        await message.channel.send(embed=embed)
    elif message.content.startswith(':데려오기'):
        embed = discord.Embed(title="데려오는 중!!", description="https://discord.com/api/oauth2/authorize?client_id=757397292390154271&permissions=8&scope=bot", color=0x62c1cc)
        embed.set_footer(text="주의 사항!! : '펭구 관리자' 역할을 만들어주세요")
        await message.channel.send(embed=embed)

    elif message.content.startswith('펭구 도움'):
        embed = discord.Embed(title="도움(명령어!)", description="펭구를 부를땐 '펭구야'라고 해주세요\n:가르치기 [물어보기];[대답]\n:잊어버려 [물어보기];[대답]\n:버전\n\n관리자 명령어\n:글로벌채팅 [켜기/끄기]\n:글로벌채팅 접속리스트\n:지우기 [개수]\n:배운것들\n:욕설리스트\n:공지 [만들기/보내기 [공지번호]]\n\n게임\n:소설 [보기/쓰기]", color=0x62c1cc)
        await message.channel.send(embed=embed)
    
    elif message.content.startswith(':홍보하기'):
        embed = discord.Embed(title="울랄라시", description="https://discord.gg/bQup75a\n게임방입니다..", color=0x62c1cc)
        await message.channel.send(embed=embed)

    elif message.content.startswith(':버전'):
        embed = discord.Embed(title="DISCORD_BOT_PENGU(%s)" % ver, description="UPDATE : {0}".format(last_update), color=0x62c1cc)
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


    for i in range(len(message.author.roles)):
        if message.author.roles[i].name == '펭구 관리자':

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

            elif message.content.startswith(':배운것들'):
                await message.channel.send(study)
                await message.delete()

            elif message.content.startswith(':끄기') and message.author.name in op_name:
                embed = discord.Embed(title="끄기", description="봇 멈춤", color=0x62c1cc)
                await message.channel.send(embed=embed)
                go = False
            
            elif message.content.startswith(':업데이트') and message.author.name in op_name:
                embed = discord.Embed(title="업데이트", description="새로운 버전을 적용합니다", color=0x62c1cc)
                await message.channel.send(embed=embed)
                subprocess.call('restart.bat')
                exit()
            
            elif message.content.startswith(':파일 업로드') and message.author.name in op_name:
                embed = discord.Embed(title="파일 업로드", description="파일 업로드 시작합니다", color=0x62c1cc)
                await message.channel.send(embed=embed)
                go = False
                subprocess.call('file_upload.bat')
                go = True

                
            

            elif message.content.startswith(':공지 '):
                if message.content[4:7] == "만들기":
                    text = message.content[8:]
                    everyone_list.append(text)
                    embed = discord.Embed(title="공지 만들기", description="공지 설정이 끝났습니다\n공지번호 : {0}".format(len(everyone_list)), color=0x62c1cc)
                    await message.channel.send(embed=embed)
                    with open("text_everyone.txt","wb") as fw: #쓰기
                        pickle.dump(everyone_list, fw)
                elif message.content[4:7] == "보내기":
                    num = message.content[8:]
                    await message.delete()
                    embed = discord.Embed(title="공지", description=str(everyone_list[int(num) - 1]), color=0x62c1cc)
                    await message.channel.send("@everyone",embed=embed)
            
            elif message.content.startswith(':글로벌채팅 '):
                text = message.content[7:]
                if text == "켜기":
                    channel = message.channel
                    channel_id = str(message.channel.id)
                    global_chet['list'].append([channel_id,channel, message.guild.member_count, message.guild.name])
                    global_chet[channel_id] = True
                    embed = discord.Embed(title="글로벌채팅 설정", description="글로벌채팅 설정이 완료되었습니댜\n글로벌 채팅에서는 봇의 채팅이 다른서버에 보이지 않습니다", color=0x62c1cc)
                    await message.channel.send(embed=embed)
                elif text == "끄기":
                    channel = message.channel
                    channel_id = str(message.channel.id)
                    global_chet['list'].remove([channel_id,channel, message.guild.member_count, message.guild.name])
                    del global_chet[channel_id]
                    embed = discord.Embed(title="글로벌채팅 설정", description="글로벌채팅이 꺼졌습니다", color=0x62c1cc)
                    await message.channel.send(embed=embed)
                elif text == "접속리스트":
                    result = ""
                    member_num = 0
                    for i in range(len(global_chet['list'])):
                        result += str(global_chet['list'][i][3]) + " / " + str(global_chet['list'][i][1].name) + "\n"
                        member_num += int(global_chet['list'][i][2])
                    embed = discord.Embed(title="글로벌채팅 리스트", description=result, color=0x62c1cc)
                    embed.set_footer(text="접속중인 서버 수 : {0} , 유저 수 : {1}".format(i + 1, member_num))
                    await message.channel.send(embed=embed)


                    







bot.run(token)
