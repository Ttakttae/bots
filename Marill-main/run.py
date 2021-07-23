import asyncio, discord, random, time, pickle, subprocess
from discord.ext import commands


# > 변수
checking = False

master_ID = [] # 개발 명령어 사용가능한 아이디
player_list = []
player_Info = {}
with open("save/player_Info", 'rb') as f:
    player_list = pickle.load(f)
    player_Info = pickle.load(f)

# ========================================================


# > 클래스, 함수
def m_to_id(text):
    if "!" in text:
        return text[3:-1]
    elif "@" in text: 
        return text[2:-1]
    else: return text

# 게임
class Game:
    def __init__(self, game_code):
        if game_code == 0: #복권
            self.lotto_card = {}
            self.bok = True
            self.bok_num_msg = None
        



# 유저
class User:
    # 기본 세팅
    def set_up(self, Id, money, role, playing_game):
        self.money = money
        self.role = role
        self.game_info = {}
        self.id = Id
        self.playing_game = playing_game


    def Info(self):
        return {'id' : self.id, 'game_info' : self.game_info, 'playing_game' : self.playing_game, 'money' : self.money, 'role' : self.role}

    # 직업 레벨업
    def role_change(self):

        if self.id in master_ID:
            self.role = "개발자"

        elif self.money < 1000000:
            self.role = "흙수저"

        elif self.money < 100000:
            self.role = "일회용수저"

        elif self.money < 500000:
            self.role = "쇠수저"
        
        elif self.money < 1500000:
            self.role = "동수저"
        
        elif self.money < 5000000:
            self.role = "은수저"
        
        elif self.money < 10000000:
            self.role = "금수저"
        
        elif self.money < 20000000:
            self.role = "다이아수저"
        
        elif self.money < 40000000:
            self.role = "타파이트수저"
        
        elif self.money < 80000000:
            self.role = "unknowned"
        else:
            self.role = "화석수저" # 1000억 이상

            #결론 수저
        
        
# ========================================================

# > 변수
player = {}
for n in player_list:
    player[n] = User()
    player[n].set_up(money = player_Info[n]['money'], Id = player_Info[n]['id'], role = player_Info[n]['role'], playing_game = player_Info[n]['playing_game'])

#복권
lotto = Game(game_code=0)
bok_card = lotto.lotto_card

# > 봇 가동
#토큰
token = ''

#설정
game = discord.Activity(type=discord.ActivityType.listening, name=";명령어")
bot = commands.Bot(command_prefix="@;@", status=discord.Status.online,activity=game, help_command=None)
client = discord.Client()

#시작
@bot.event
async def on_ready():
    print("=============START=============")
    

#채팅
@bot.event
async def on_message(message):
    global checking

    with open("save/master_ID", 'r') as f:
        while True:
            data = f.readline()
            if not data:
                break
            else: master_ID.append(data[:-1])
    
    # 봇 메시지 무시
    if message.author.bot:
        return None
    
    # 변수
    channel = message.channel #메시지 수신 채널
    content = message.content #메시지 내용
    author = message.author #수신자
    author_id = str(author.id)

    # 신규 가입
    if not author_id in player:
        player_list.append(author_id)
        player[author_id] = User()
        player[author_id].set_up(Id = author_id, money = 50000, role = "흙수저", playing_game = None)
        print("%s 가입" % author)

    # 복권 (2일 후 없어지는 거)
    delete_bok = []
    bk_today = int(time.strftime('%d', time.localtime(time.time())))
    for key in bok_card.keys():
        if bk_today != int(bok_card[key][5][-2:]):
            if bok_card[key][0].content[3:4] == "F":
                embed=discord.Embed(title="복권", description = "***4000 원***")
                await bok_card[key][0].edit(content = "복권을 긁지 않아 환불되었습니다", embed = embed)
                player[bok_card[key][3]].money += 4000
            else:
                embed=discord.Embed(title="복권", description = "***%i 원***" % bok_card[key][1])
                await bok_card[key][0].edit(content = "지급받지 않아 자동으로 지급되었습니다", embed = embed)
                player[bok_card[key][3]].money += bok_card[key][1]
            delete_bok.append(key)
    for key in delete_bok:
        del bok_card[key]

    
    # 플레이어 변수
    user = player[author_id]

    # 플레이어 업데이트
    user.role_change()

    # 명령어 감지
    if content.startswith(';'):
        
        if checking and not author_id in master_ID:
            await channel.send("지금은 점검중 입니다")
            return None


        # 띄어쓰기 단위로 명령어 쪼개기
        content = content[1:]
        cmd = [] # 결과
        start = 0
        for n in range(len(content)):
            if content[n:n+1] == " ":
                cmd.append(content[start:n])
                start = n + 1
            if n + 1 == len(content):
                cmd.append(content[start:])
        

        # > 명령어
        
        # 개발자 명령어
        if author_id in master_ID:

            # 원격 업데이트

            if cmd[0]  == "업데이트":
                await channel.send("업데이트 시작")
                subprocess.call("update_bot.bat")
                exit()
                
            elif cmd[0]  == "파일저장":
                await channel.send("파일 업로드 시작")
                subprocess.call("save_files.bat")
                
            elif cmd[0]  == "종료":
                await channel.send("시스템이 종료됩니다")
                exit()
            
            elif cmd[0] == "지급":
                player[str(m_to_id(cmd[1]))].money += int(cmd[2])
                await channel.send("%s원 지급완료" % cmd[2])
            
            elif cmd[0] == "점검":
                checking = True
                await channel.send("점검 시작")
                delete_bok = []
                for key in bok_card.keys():
                        if bok_card[key][0].content[3:4] == "F":
                            embed=discord.Embed(title="복권", description = "***4000 원***")
                            await bok_card[key][0].edit(content = "복권을 긁지 않아 환불되었습니다", embed = embed)
                            player[bok_card[key][3]].money += 4000
                        else:
                            embed=discord.Embed(title="복권", description = "***%i 원***" % bok_card[key][1])
                            await bok_card[key][0].edit(content = "지급받지 않아 자동으로 지급되었습니다", embed = embed)
                            player[bok_card[key][3]].money += bok_card[key][1]
                        delete_bok.append(key)
                for key in delete_bok:
                    del bok_card[key]
                
            
            elif cmd[0] == ";복권":
                if cmd[1] == "개수":
                    msg = await channel.send("실시간 복권 개수 : %i개" % len(bok_card))
                    lotto.bok_num_msg = msg
                elif cmd[1] == "켜기":
                    lotto.bok = True
                    await channel.send("복권 활성화")
                elif cmd[1] == "끄기":
                    lotto.bok = False
                    await channel.send("복권 비활성화")
            

        if cmd[0] == "명령어" or cmd[0] == "ㅁㄹㅇ" or cmd[0] == "afd":
            embed = discord.Embed(title="명령어", description="[여기](<%s>)를 눌러 명령어를 보러가세요!" % 'https://discord.gg/Pvak62UVYS', color=0xacf6f1)
            await channel.send(embed = embed)
            


        elif cmd[0] == "정보" or cmd[0] == "ㅈㅂ" or cmd[0] == "wq":
            field_list = [['돈', "`%i 원`" % user.money]]
            embed=discord.Embed(title="%s(%s)" % (str(author), user.role))
            for n in range(len(field_list)):
                embed.add_field(name=field_list[n][0], value=field_list[n][1], inline=True)
            await channel.send(embed = embed)
        

        
        elif cmd[0] == "복권" or cmd[0] == "ㅂㄱ" or cmd[0] == "qr":
            if lotto.bok == False and not author_id in master_ID:
                await channel.send("현재 복권이 비활성화된 상태입니다")
                return None
            if user.money < 4000:
                await channel.send("돈이 없습니다[<@%s>]" % (str(author_id)))
                return None
            user.money -= 4000
            rand_n = random.randint(1, 100)
            if rand_n <= 60: # 60%
                n = 2000
            elif rand_n <= 80: # 20%
                n = 8000
            elif rand_n <= 95: # 15%
                n = 13000
            elif rand_n <= 100: # 5%
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
            
            msg = await channel.send("(tip : 복권을 열지 않으면 2일 후에 만료됩니다)")
        
            await msg.add_reaction("✅")
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
            await msg.add_reaction("3️⃣")
            await msg.add_reaction("4️⃣")

            bok_card[bok_id] = [msg, n, {1:"⬜⬜",2:"⬜⬜",3:"⬜⬜",4:"⬜⬜"}, str(author_id), icon, time.strftime('%Y%m%d', time.localtime(time.time()))]
            embed = discord.Embed(title="복권 - %s" % (str(author)), description="⬜⬜ | 2000원\n⬜⬜ | 8000원\n⬜⬜ | 13000원\n⬜⬜ | 20000원", color=0xacf6f1)
            embed.set_footer(text="1️⃣2️⃣3️⃣4️⃣ : 열기, ✅ : 보상 받기")
            await msg.edit(content = "B0-F-%i-%s" % (bok_id, author_id),embed = embed)
            try:
                await lotto.bok_num_msg.edit(content = "실시간 복권 개수 : %i개" % len(bok_card))
            except: pass

        # ========================================================

        # > 플레이어 정보 저장
        player_Info = {}
        for n in player_list:
            player_Info[n] = player[n].Info()
        with open("save/player_Info", 'wb') as f:
            pickle.dump(player_list, f)
            pickle.dump(player_Info, f)
        # ========================================================

        # > 로그
        #명령어 사용내역만 출력
        print("{0}/{1}/{2}({3}) : {4}".format(message.guild.name, message.channel.name ,author, author_id, str(content)))
        
        # 채팅 저장
        with open('save/chet_log', 'a', encoding = 'UTF-8') as f:
            f.write("\n{0}/{1}({2}) : {3}".format( time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) , author, author_id, str(content)))
        # ========================================================



# 리엑션 버튼
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot == 1:
        return None
    
    if reaction.message.content[:2] == "B0":
        bok_id = int(reaction.message.content[5:9])
        player_id = str(reaction.message.content[10:])

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
            gold = 8000
        if reaction.emoji == "3️⃣":
            choice = 3
            gold = 13000
        if reaction.emoji == "4️⃣":
            choice = 4
            gold = 20000
        
        if reaction.emoji == "✅":
            embed = discord.Embed(title="복권", description="***%i 원***" % n, color=0xacf6f1)
            await bok_card[bok_id][0].edit(content = "",embed = embed)
            player[str(user.id)].money += n
            
            del bok_card[bok_id]
            try:
                await lotto.bok_num_msg.edit(content = "실시간 복권 개수 : %i개" % len(bok_card))
            except: pass
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

        embed = discord.Embed(title="복권 - %s" % (str(user)), description="{0} | 2000원\n{1} | 8000원\n{2} | 13000원\n{3} | 20000원".format(bok_card[bok_id][2][1], bok_card[bok_id][2][2], bok_card[bok_id][2][3], bok_card[bok_id][2][4]), color=0xacf6f1)
        embed.set_footer(text="1️⃣2️⃣3️⃣4️⃣ : 열기, ✅ : 보상 받기")
        await bok_card[bok_id][0].edit(content = "B0-T-%i-%s" % (bok_id, player_id), embed = embed)
    




bot.run(token)

# ========================================================
