# 끝말잇기
import random

# word파일
# 단어가 적혀있음
# 마지막 단어는 항상 엔터 쳐야됨

# custom 파일
# 마지막 항상 엔터
# 1 : 봇 이름
# 2 : 플레이어 이름
# 3 : 랜덤 단어 밴 개수(난이도를 위해서 만듦)
# 4 : study의 유무 => 1이면 게임중 모르는 단어를 기억함, 테스트용으로는 0
# 5 : 제한의 유무 => 1이면 봇이 아는 단어 안에서 게임진행
# 6 : shuffle 유무 => 1이면 shuffle 됨, 단어 우선순위에 대한 shuffle


import random

# word파일 읽기
words = [] # 단어 저장

f = open('word', 'r', encoding='utf-8')
while True:
    data = str(f.readline())
    if not data:
        break
    words.append(data[:-1])
f.close()

# print(words)

# custom파일 읽기
custom = {}
custom_count = 6

f = open('custom', 'r', encoding='utf-8')
for custom_num in range(custom_count):
    data = str(f.readline())[:-1]
    
    if custom_num == 0:
        custom['name'] = data
    if custom_num == 1:
        custom['nameP'] = data
    if custom_num == 2:
        custom['ban_word'] = int(data)
    if custom_num == 3:
        custom['study'] = int(data)
    if custom_num == 4:
        custom['dicIn'] = int(data)
    if custom_num == 5:
        custom['Rshuffle'] = int(data)
f.close()

# print(custom)

# custom 세팅
ban_word = []
for i in range(custom['ban_word']):
    while True:
        append_word = random.choice(words)
        if append_word in ban_word:
            pass
        else:
            ban_word.append(append_word)
            break

# print(ban_word)


# 5
if custom['Rshuffle'] == 1:
    random.shuffle(words)

# 게임

used_words = []

while True:
    player_word = str(input("{0} >> ".format(custom['nameP'])))
    if player_word == "":
        print("------------\n패배\n------------")
        break

    player_word_link = player_word[-1:]
    
    #try:
        #if not bot_word_link == player_word_link: #여기 부분 오류 있는거 아님
            #print("첫 글자가 다름")
            #continue
    #except: pass

    if player_word not in words and custom['dicIn'] == 1:
        print("사전에 없는 단어")
        continue
    
    if len(player_word) == 1:
        print("한 글자 단어")
        continue

    if player_word in used_words:
        print("이미 사용된 단어")
        continue
    # print(player_input)
    used_words.append(player_word)

    # 저장
    if not player_word in words and custom['study'] == 1:
        words.append(player_word)
    
    bot = False
    for word in words:
        if word[:1] == player_word_link and not word in used_words and not word in ban_word:
            bot = True
            used_words.append(word)
            #bot_word_link = word[-1:]
            print("{0} >> {1}".format(custom['name'], word))
            break
    if bot == False:
        print("------------\n승리\n------------")
        break

f = open('word', 'w', encoding='utf-8')
for word in words:
    f.write(word + "\n")
# print("저장완료")
