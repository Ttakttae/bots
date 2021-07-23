import asyncio, discord, os, pickle, random, time, subprocess
from discord.ext import commands

###########################################
last_update = {'ED' : ['버전 GUI', '로또 GUI', '로또 기능 추가','로또 맨션', '로또 등록개수 수정','로또 중복순위 수정',  '펭구베타 기능', '개인메시지 기능 추가', '펭구 도움 리메이크'], 'HP' : ['로또 등록 메시지 오류 수정', '로또 중복순위 재오류 수정', '로또 설명문 추가', '펭구베타테스터 안들어가지는 문제'], 'F' : "False", 'ER': [], 'EVT' : ['로또', '중고BETA']}
ver = "v1.9"
"""다음 버전: 예외 줄이기//릴레이 소설 앨범만들기//GUI UPDATE"""
op_name = ['Pio', 'Windows 10', 'Codedis'] #최고 관리자
###########################################
event = False





with open("bad_list.txt","rb") as fr: #읽기
    bad_list = pickle.load(fr)
with open("study.txt","rb") as fr: #읽기
    study = pickle.load(fr)
with open("text_everyone.txt","rb") as fr: #읽기
    everyone_list = pickle.load(fr)
with open("lolling.txt","rb") as fr: #읽기
    lolling_list = pickle.load(fr)
with open("EVENT\\LOTTO\\lotto_nums.txt","rb") as fr: #읽기
    lotto_list = pickle.load(fr)


global_chet = {'list':[]}


#토큰
token = 'token'
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
    global go, ver, last_update, op_name, lotto_list, event, player_info, item_info, lolling_list
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
            embed = discord.Embed(title="베타 테스트", description="[참여하기](<%s>)" % 'https://discord.gg/xXVFgTH', color=0x62c1cc)
            embed.set_footer(text="5초 후 이 메시지는 없어집니다")
            msg = await message.channel.send(embed=embed)
            time.sleep(5)
            await msg.delete()
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
                embed = discord.Embed(title="", description=":bangbang: 욕설을 하시면 경고를 받습니당~\n ||대상:<@{0}> 부르기: @펭구 관리자 ||".format(message.author.id), color=0x62c1cc)
                delete_msg = await message.channel.send(embed=embed)
                await message.delete()
        await bot.process_commands(message)
    print("{0}/{1}/{2} : {3}".format(message.guild.name,message.channel.name,message.author.name,str(message.content)))
    if message.content.startswith('펭구야 '):
        return None
        if message.content[4:] in study:
            await message.channel.send(study[message.content[4:]][random.randint(0, len(study[message.content[4:]]) -1)])
        else:
            await message.channel.send('?')
    elif message.content.startswith(':가르치기 '):
        return None
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
        return None
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

    elif message.content.startswith('펭구야'):
        await message.channel.send('?')

    elif message.content.startswith(':데려오기'):
        embed = discord.Embed(title="데려오는 중!!", description="[데려가는 곳](<%s>)" % 'https://discord.com/api/oauth2/authorize?client_id=757397292390154271&permissions=8&scope=bot', color=0x62c1cc)#-------------------------------------------------------------
        embed.set_footer(text="주의 사항!! : '펭구 관리자' 역할이 새로 생깁니다!")#-------------------------------------------------------------
        await message.channel.send(embed=embed)

    elif message.content.startswith('펭구 도움'):
        page = ['펭구를 부를땐 "펭구야"라고 해주세요\n```:가르치기 [물어보기];[대답]```\n```:잊어버려 [물어보기];[대답]```\n```:버전```', '개인메시지 명령어\n```펭구베타```\n```펭구코드```', '관리자 명령어\n```:글로벌채팅 [켜기/끄기]```\n```:글로벌채팅 접속리스트```\n```:지우기 [개수]```\n```:배운것들```\n```:욕설리스트```\n```:공지 [만들기/보내기 [공지번호]]```']
        embed = discord.Embed(title=":scroll: 도움(명령어!)", description=page[0], color=0x62c1cc)
        embed.set_footer(text="◀️:이전장 ▶️:다음장 ❌:끄기")
        msg = await message.channel.send("페이지[0]", embed=embed)
        await msg.add_reaction('▶️')
        await msg.add_reaction('❌')
    
    elif message.content.startswith(':홍보하기'):
        embed = discord.Embed(title="울랄라시", description="https://discord.gg/bQup75a\n게임방입니다..", color=0x62c1cc)
        await message.channel.send(embed=embed)
        
    elif message.content.startswith(':로또 '):
        if message.author.name:
            txt = message.content[4:6]
            if txt == "정보":
                embed = discord.Embed(title="정보", description="사람당 하루에 2개씩 등록이 가능합니다```:로또 등록 [번호]```\n번호는 1~6까지 이며 6자리 입력을 하시면 됩니다(중복X)\n\n1등 : 10000원 문상, 2등 : 5000원 문상\n\n```현 최대 등록 개수 : 12개```\n\n기간 : 10/11부터 10/17까지", color=0x62c1cc)
                await message.channel.send(embed=embed)
            if txt == "보기":
                for i in range(len(lotto_list[0])):
                    if lotto_list[0][i] == str(message.author.id):
                        num = i
                result = ""
                for i in lotto_list[1][num]:
                    result += str(i) + "\n"
                embed = discord.Embed(title="보기", description=result, color=0x62c1cc)
                await message.channel.send(embed=embed)


            elif txt == "등록":
                if event == False:
                    embed = discord.Embed(title="종료된 이벤트", description="이미 종료된 이벤트 입니다", color=0x62c1cc)
                    await message.channel.send(embed=embed)
                    return None
                num = message.content[7:]
                #id = [ [id], [ [code1, code2, code3], [code1, code2, code 3] ] ]
                if len(num) == 6:
                    findnum = ['1', '2', '3', '4', '5', '6']
                    dup = 0
                    for i in range(len(num)):
                        if num[i] in findnum:
                            findnum.remove(num[i])
                        else:
                            dup += 1
                    if not dup == 0:
                        embed = discord.Embed(title="로또 번호 등록", description="<@{0}>\n등록 번호에 {1}개의 중복되거나 1~6범위 안에 없는 수가 있습니다".format(message.author.id, dup), color=0x62c1cc)
                        await message.channel.send(embed=embed)
                        return None
                    if not str(message.author.id) in lotto_list[0]:
                        lotto_list[0].append(str(message.author.id))
                        lotto_list[1].append([])
                    for i in range(len(lotto_list[0])):
                        if lotto_list[0][i] == str(message.author.id):
                            codes = i
                            print(codes)
                    if len(lotto_list[1][codes]) < 12 and not num in lotto_list[1][codes]:
                        lotto_list[1][codes].append(num)
                        print(lotto_list)
                        await message.delete()
                        embed = discord.Embed(title="로또 번호 등록", description="등록되었습니다!", color=0x62c1cc)
                        embed.set_author(name="%s" % str(message.author.name),icon_url=message.author.avatar_url)
                        await message.channel.send(embed = embed)
                        with open("EVENT\LOTTO\lotto_nums.txt","wb") as fw:
                            pickle.dump(lotto_list, fw)
                    else:
                        if num in lotto_list[1][codes]:
                            embed = discord.Embed(title="로또 번호 등록", description="<@{0}>\n같은 번호를 여러번 등록할 수 없습니다!!".format(message.author.id), color=0x62c1cc)
                            await message.channel.send(embed=embed)
                        else:
                            embed = discord.Embed(title="로또 번호 등록", description="<@{0}>\n최대 12개까지 등록할 수 있어요(최대 등록 개수 초과, 내일 다시 시도해보세요)".format(message.author.id), color=0x62c1cc)
                            await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="로또 번호 등록", description="<@{0}>\n등록 번호가 6자리보다 짧거나 길어요".format(message.author.id), color=0x62c1cc)
                    await message.channel.send(embed=embed)

            elif txt == "결과" and message.author.name in op_name:
                with open('EVENT\\LOTTO\\num.txt', 'r') as f:
                    num = f.read()
                first = num
                first_name = ""
                second = num[:4]
                second_name = ""
                third = num[:3]
                third_name = ""
                fourth = num[:2]
                fourth_name = ""
                fifth = num[:1]
                fifth_name = ""
                for n in range(len(lotto_list[0])):
                    jong = [1,2,3,4,5]
                    for m in range(len(lotto_list[1][n])):
                        print(n, m)
                        if str(lotto_list[1][n][m]) == first:
                            if 1 in jong:
                                first_name += "<@%s> " % lotto_list[0][n]
                                jong.remove(1)
                        elif str(lotto_list[1][n][m][:4]) == second:
                            if 2 in jong:
                                second_name += "<@%s> " % lotto_list[0][n]
                                jong.remove(2)
                        elif str(lotto_list[1][n][m][:3]) == third:
                            if 3 in jong:
                                third_name += "<@%s> " % lotto_list[0][n]
                                jong.remove(3)
                        elif str(lotto_list[1][n][m][:2]) == fourth:
                            if 4 in jong:
                                fourth_name += "<@%s> " % lotto_list[0][n]
                                jong.remove(4)
                        elif str(lotto_list[1][n][m][:1]) == fifth:
                            if 5 in jong:
                                fifth_name += "<@%s> " % lotto_list[0][n]
                                jong.remove(5)

                embed = discord.Embed(title=":scroll: 로또 결과", description=":one:  : {0}\n\n:two:  : {1}\n\n:three:  : {2}\n\n:four:  : {3}\n\n:five:  : {4}".format(first_name, second_name, third_name, fourth_name, fifth_name), color=0x62c1cc)
                await message.channel.send(embed=embed)

            elif txt == "번호" and message.author.name in op_name:
                await message.channel.send(lotto_list)

            elif txt == "종료" and message.author.name in op_name:
                await message.channel.send("이벤트 종료")
                event = False
            
            elif txt == "시작" and message.author.name in op_name:
                await message.channel.send("이벤트 시작")
                event = True


            elif txt == "리셋" and message.author.name in op_name:
                with open("EVENT\LOTTO\lotto_nums.txt","wb") as fw:
                    pickle.dump([[], []], fw)
                lotto_list = [[], []]
                await message.channel.send("번호 리셋 완료")
            ##여기--------------------------------------------------------------------------------------
            elif txt == "뽑기" and message.author.name in op_name:
                go = False
                await message.channel.send("번호 뽑기를 시작합니다")
                num_icon = [':one: ',':two: ',':three: ',':four: ',':five: ',':six: ']
                num_list = [1,2,3,4,5,6]
                result = ""
                result_num = ""
                embed = discord.Embed(title="번호", description="뽑는중 !!", color=0x62c1cc)
                num_msg = await message.channel.send(embed=embed)
                while True:
                    randnum = random.randint(1, 6)
                    if randnum in num_list:
                        time.sleep(2)
                        await num_msg.delete()
                        num_list.remove(randnum)
                        print(num_list, randnum, num_icon)
                        result_num += str(randnum)
                        result += num_icon[int(randnum - 1)]
                        embed = discord.Embed(title="번호 뽑는중", description="%s" % result, color=0x62c1cc)
                        num_msg = await message.channel.send(embed=embed)
                    elif len(num_list) == 0:
                        break
                await num_msg.delete()
                embed = discord.Embed(title="최종 결과", description="%s" % result, color=0x62c1cc)
                num_msg = await message.channel.send(embed=embed)
                with open("EVENT\\LOTTO\\num.txt","w") as fr: #읽기
                    fr.write(result_num)
                go = True



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


                    




@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        return None
    if str(reaction.message.content[:3]) == "페이지":
        page = ['펭구를 부를땐 "펭구야"라고 해주세요\n```:가르치기 [물어보기];[대답]```\n```:잊어버려 [물어보기];[대답]```\n```:버전```\n```:데려오기```', '게임\n```:로또 [정보/등록[번호]/보기]```\n```:소설 [보기/쓰기]```', 'DM명령어\n```펭구베타```\n```펭구코드```', '관리자 명령어\n```:글로벌채팅 [켜기/끄기]```\n```:글로벌채팅 접속리스트```\n```:지우기 [개수]```\n```:배운것들```\n```:욕설리스트```\n```공지기능 : ⤴️을 메시지 보내고 달으면 됩니다```']
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
