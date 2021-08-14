import asyncio, youtube_dl, discord, yt_search, time, googleapiclient
from discord_slash import SlashCommand, SlashContext
from googleapiclient import discovery
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord_slash.utils.manage_commands import create_option


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
option = {
    'extractaudio':True,
    'audioformat':'mp3',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}


# scripts
from scripts.music_player import *
from scripts.music_playlist import *
from scripts.language import *



token = "" # 토큰키
google_api_key = ""
print(token)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
slash = SlashCommand(client, sync_commands=True)
### 클래스------------------###


lng = Language()
lng.load_all_language()
lng.load_server_language()

mp_dic = {}
### -----------------------###

### playlist 함수------------###

async def add_playlist_videos(video_key, voice_channel, author_id, channel):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = google_api_key)

    request = youtube.playlistItems().list(part = "snippet", playlistId = video_key)
    response = request.execute()

    playlist_items = []
    video_ids = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    for t in playlist_items:
        video_ids.append(t["snippet"]["resourceId"]["videoId"])

    for vi in video_ids:
        url = "https://www.youtube.com/watch?v={}".format(vi)
        with youtube_dl.YoutubeDL(option) as ydl:
            information = ydl.extract_info(url, download=False)
        audio_url = information['formats'][0]['url']
        title = information["title"]
        length = information['duration']
        add_playlist(voice_channel, vi, title, length, author_id, audio_url, title)

async def downloading(url):
    with youtube_dl.YoutubeDL(option) as ydl:
        information = ydl.extract_info(url, download=False)
    return information

### ------------------------###

@slash.slash(name="ping", description="pong!")
async def ping(message):
    await message.send(content=f"Pong! {client.latency*1000}ms")

@slash.slash(name="제작진", description="만든이")
async def madeby(message):
    await message.send(content=lng.tl("made_by", str(message.guild.id)))

@slash.slash(name="입장", description="음성 채널에 입장합니다")
async def join(message):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))

    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        try:
            await message.author.voice.channel.connect()
            await message.send(content=lng.tl("voice.connect", str(message.guild.id)).format(voice_channel))
        except:
            await message.send(content=lng.tl("no.permission", str(message.guild.id)))
        else:
            mp_dic[str(message.channel.id)] = music_playing()
        finally:
            pass

@slash.slash(name="퇴장", description="음성채널에서 나갑니다")
async def leave(message):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc

        reset_channel_playlist(voice_channel)

        await voice.disconnect()
        await message.send(content=lng.tl("voice.disconnect", str(message.guild.id)).format(voice_channel))
        try:
            await mp_dic[str(message.channel.id)].task_kill()
        except:
            pass

        del mp_dic[str(message.channel.id)]

@slash.slash(name="재생", description="노래를 재생합니다", options=[create_option(name="song", description="유튜브 링크나 검색 키워드(라이브 스트리밍, 플레이리스트, 그냥 동영상 모두 가능)", option_type=3, required=True)])
async def play(message, song: str):
    url = song
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        try: # 오류 방지
            await message.author.voice.channel.connect()
            await message.send(content=lng.tl("voice.connect", str(message.guild.id)).format(voice_channel))
            mp_dic[str(message.channel.id)] = music_playing()
        except:
            pass

        for vc in client.voice_clients:
            channel_list = vc.channel
            if vc.guild == message.guild:
                voice = vc

        ### mp3 다운로드-----------###
        url_search = False
        playlist_search = False
        not_youtube_search = False
        if "https://" in url:
            if "youtu.be" in url: # 인풋받은 링크가 모바일 유튜브 링크인가?
                video_key = url.split("/")[3]
                url_search = True
            elif "playlist" in url:
                video_key = url.split("=")[1]
                playlist_search = True
                url_search = False
            else:
                try:
                    video_key = url.split("=")[1]
                    try:
                        video_key = video_key.replace("&list", "")
                    except:
                        pass
                    url_search = True
                except:
                    url_search = False
                    not_youtube_search = True

        else:
            video_key = url

        if url_search:
            await message.send(content=lng.tl("finding.song", str(message.guild.id)))
            url = "https://www.youtube.com/watch?v={}".format(video_key)
            information = await downloading(url)
            await asyncio.sleep(1)
            audio_url = information['formats'][0]['url']
            title = information["title"]
            length = information['duration']
            add_playlist(voice_channel, video_key, title, length, message.author.id, audio_url, title)

        elif not_youtube_search:
            information = await downloading(url)
            await asyncio.sleep(1)
            audio_url = information['formats'][0]['url']
            title = information["title"]
            try:
                length = information['duration']
                video_key = url.split("/")[4]
                await asyncio.sleep(2)
            except:
                length = 0
                video_key = url.split("/")[3]
                await asyncio.sleep(2)
            add_playlist(voice_channel, video_key, title, length, message.author.id, audio_url, title)

        elif playlist_search:
            await message.send(content=lng.tl("cheking.playlist", str(message.guild.id)))
            await add_playlist_videos(video_key, voice_channel, message.author.id, message)
            await message.send(content=lng.tl("playlist.add", str(message.guild.id)))
            await asyncio.sleep(3)

        else: # keyword search!
            await message.send(content=lng.tl("finding.song", str(message.guild.id)))
            yt = yt_search.build(google_api_key)
            search_result = yt.search("{}".format(video_key), sMax=10, sType=["video"])
            try:
                search_result.videoId.remove(None)
            except:
                pass
            video_key = search_result.videoId[0]
            url = "https://www.youtube.com/watch?v={}".format(video_key)
            information = await downloading(url)
            await asyncio.sleep(1)
            audio_url = information['formats'][0]['url']
            title = information["title"]
            length = information['duration']
            add_playlist(voice_channel, video_key, title, length, message.author.id, audio_url, title)

        if not vc.is_playing():
            source = FFmpegPCMAudio(playlist[voice_channel]["list"][0]["audio_url"], **FFMPEG_OPTIONS)# converts the youtube audio source into a source discord can use
            voice.play(source)  # play the source
            await message.send(content=lng.tl("voice.play", str(message.guild.id)).format(playlist[voice_channel]["list"][0]["title"])) # ``text`` 진하기로 노래 제목 강조
            if playlist[voice_channel]["list"][0]["length"] == 0:
                pass
            else:
                await mp_dic[str(message.channel.id)].create_task(voice, voice_channel, message, playlist, str(message.guild.id))
        else:
            await message.send(content=lng.tl("song.add", str(message.guild.id)))

@slash.slash(name="일시정지", description="노래를 잠시 중지합니다")
async def pause(message):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild = message.guild) #봇의 음성 관련 정보
        if voice.is_playing(): #노래가 재생중이면
            if playlist[voice_channel]["list"][0]["length"] == 0:
                pass
            else:
                time[voice_channel]["paused-time"] = time[voice_channel]["now-remaining"]
                playlist[voice_channel]["list"][0]["length"] = time[voice_channel]["paused-time"]
                await mp_dic[str(message.channel.id)].task_kill()

            voice.pause() #일시정지
            await message.send(content=lng.tl("voice.pause", str(message.guild.id)))
        else:
            await message.send(content=lng.tl("voice.pause.voice_not_playing", str(message.guild.id)))

@slash.slash(name="다시재생", description="노래를 다시 재생합니다")
async def resume(message):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        voice = discord.utils.get(client.voice_clients, guild = message.guild) #봇의 음성 관련 정보
        if voice.is_paused(): #일시정지 상태이면
            voice.resume()
            await message.send(content=lng.tl("voice.replay", str(message.guild.id)))
            if playlist[voice_channel]["list"][0]["length"] == 0:
                pass
            else:
                await mp_dic[str(message.channel.id)].create_task(voice, voice_channel, message, playlist, str(message.guild.id))
        else:
            await message.send(content=lng.tl("voice.replay.voice_playing", str(message.guild.id)))

@slash.slash(name="재생목록", description="재생목록을 보여줍니다")
async def queue(message):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        check_channel_playlist(voice_channel)

        result = ""
        for playlist_number, music_info in enumerate(playlist[voice_channel]["list"]):
            result += "{}. {} queued by <@{}>\n".format(playlist_number + 1, music_info["video_title"], music_info["author"])
        result = result[:-1]


        embed = discord.Embed(title = lng.tl("voice.playlist.title", str(message.guild.id)).format(playlist[voice_channel]["loop"]), description = "{}".format(result), color = 0xECDDC3)
        await message.send(embed = embed)

@slash.slash(name="건너뛰기", description="노래를 건너뜁니다")
async def skip(message):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc

        if playlist_music_count(voice_channel) >= 1:
            if playlist_music_count(voice_channel) > 1 or playlist[voice_channel]["loop"] == "single" or playlist[voice_channel]["loop"] == "all":
                await message.send(content=lng.tl("voice.skip", str(message.guild.id)))
                voice.stop()
                if playlist[voice_channel]["list"][0]["length"] == 0:
                    pass
                else:
                    await mp_dic[str(message.channel.id)].task_kill()
                next_playlist(voice_channel)
                source = FFmpegPCMAudio(playlist[voice_channel]["list"][0]["audio_url"], **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
                voice.play(source)
                await message.send(content=lng.tl("voice.play", str(message.guild.id)).format(playlist[voice_channel]["list"][0]["video_title"]))
                if playlist[voice_channel]["list"][0]["length"] == 0:
                    pass
                else:
                    await mp_dic[str(message.channel.id)].create_task(voice, voice_channel, message, playlist, str(message.guild.id))
            else:
                voice.stop()
                if playlist[voice_channel]["list"][0]["length"] == 0:
                    pass
                else:
                    await mp_dic[str(message.channel.id)].task_kill()
                delete_playlist(voice_channel, 1)
                await message.send(content=lng.tl("voice.skip", str(message.guild.id)))
        else:
            await message.send(content=lng.tl("delete.no.song", str(message.guild.id)))

@slash.slash(name="삭제", description="노래를 삭제합니다", options=[create_option(name="number", description="삭제할 노래의 숫자(재생목록에 나온 숫자 기준)", option_type=4, required=True)])
async def delete(message, number: int):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))

    if author_in_voice_chanel:
        music_number = number - 1

        for vc in client.voice_clients:
            if vc.guild == message.guild:
                voice = vc

        if 1 <= music_number < playlist_music_count(voice_channel):
            await message.send(content=lng.tl("voice.delete", str(message.guild.id)).format(playlist[voice_channel]["list"][music_number]["video_title"]))
            delete_playlist(voice_channel, music_number + 1)

        elif 0 == music_number < playlist_music_count(voice_channel):
            if music_number+1 == playlist_music_count(voice_channel):
                if playlist[voice_channel]["list"][0]["length"] == 0:
                    pass
                else:
                    await mp_dic[str(message.channel.id)].task_kill()
                await message.send(lng.tl("voice.delete", str(message.guild.id)).format(playlist[voice_channel]["list"][music_number]["video_title"]))
                voice.stop()
                delete_playlist(voice_channel, music_number + 1)
                loop = "off"
                playlist_set_loop_mode(voice_channel, loop)
            else:
                if playlist[voice_channel]["loop"] == "single":
                    await message.send(content=lng.tl("voice.delete", str(message.guild.id)).format(playlist[voice_channel]["list"][music_number]["video_title"]))
                    voice.stop()
                    if playlist[voice_channel]["list"][0]["length"] == 0:
                        pass
                    else:
                        await mp_dic[str(message.channel.id)].task_kill()
                    loop = "off"
                    playlist_set_loop_mode(voice_channel, loop)
                    delete_playlist(voice_channel, music_number + 1)
                    source = FFmpegPCMAudio(playlist[voice_channel]["list"][0]["audio_url"], **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
                    voice.play(source)  # play the source
                    await message.send(content=lng.tl("voice.play", str(message.guild.id)).format(playlist[voice_channel]["list"][0]["video_title"]))
                    await asyncio.sleep(playlist[voice_channel]["list"][0]["length"]+1)
                    if playlist[voice_channel]["list"][0]["length"] == 0:
                        pass
                    else:
                        await mp_dic[str(message.channel.id)].create_task(voice, voice_channel, message, playlist, str(message.guild.id))
                else:
                    await message.send(content=lng.tl("voice.delete", str(message.guild.id)).format(playlist[voice_channel]["list"][music_number]["video_title"]))
                    voice.stop()
                    if playlist[voice_channel]["list"][0]["length"] == 0:
                        pass
                    else:
                        await mp_dic[str(message.channel.id)].task_kill()
                    delete_playlist(voice_channel, music_number + 1)
                    source = FFmpegPCMAudio(playlist[voice_channel]["list"][0]["audio_url"], **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
                    voice.play(source)  # play the source
                    await message.send(content=lng.tl("voice.play", str(message.guild.id)).format(playlist[voice_channel]["list"][0]["video_title"]))
                    await asyncio.sleep(playlist[voice_channel]["list"][0]["length"]+1)
                    if playlist[voice_channel]["list"][0]["length"] == 0:
                        pass
                    else:
                        await mp_dic[str(message.channel.id)].create_task(voice, voice_channel, message, playlist, str(message.guild.id))


        else:
            await message.send(content=lng.tl("delete.no.song", str(message.guild.id)))# 삭제하려는 노래가 플레이 리스트 범위를 넘거나 0보다 작음


@slash.slash(name="반복", description="노래 한곡이나 전체를 반복하거나, 반복을 끕니다", options=[create_option(name="mode", description="한곡: single, 전체: all, 끄기: off", option_type=3, required=True)])
async def loop(message, mode: str):
    try:
        voice_channel = message.author.voice.channel
        author_in_voice_chanel = True
    except:
        author_in_voice_chanel = False
        await message.send(content=lng.tl("enter.voice_channel", str(message.guild.id)).format(str(message.author.id)))
    if author_in_voice_chanel:
        voice_channel = message.author.voice.channel
        if mode == "single":
            if len(playlist[voice_channel]["list"]) >= 1:
                loop = "single"
                playlist_set_loop_mode(voice_channel, loop)
                await message.send(content=lng.tl("voice.loop.one", str(message.guild.id)).format(playlist[voice_channel]["list"][0]["video_title"]))
            else:
                await message.send(content=lng.tl("no.song.loop", str(message.guild.id)))

        if mode == "all":
            if len(playlist[voice_channel]["list"]) >= 1:
                loop = "all"
                playlist_set_loop_mode(voice_channel, loop)
                await message.send(content=lng.tl("voice.loop.all", str(message.guild.id)))
            else:
                await message.send(content=lng.tl("no.song.loop", str(message.guild.id)))

        if mode == "off":
            loop = "off"
            playlist_set_loop_mode(voice_channel, loop)
            await message.send(content=lng.tl("voice.loop.off", str(message.guild.id)))

@slash.slash(name="언어변경", description="출력되는 언어(slash command 이름이나 설명 아님)를 변경합니다", options=[create_option(name="language", description="다음중 선택(korean, english, chinese, japanese)", option_type=3, required=True)])
async def language_change(message, language: str):
    if language == "korean":
        lng.channel_language[str(message.guild.id)] = 'ko-KR'
        await message.send(content=lng.tl("voice.set_language", str(message.guild.id)))
        lng.save_server_language()
    elif language == "english":
        lng.channel_language[str(message.guild.id)] = 'en-US'
        await message.send(content=lng.tl("voice.set_language", str(message.guild.id)))
        lng.save_server_language()
    elif language == "chinese":
        lng.channel_language[str(message.guild.id)] = 'zh-CN'
        await message.send(content=lng.tl("voice.set_language", str(message.guild.id)))
        lng.save_server_language()
    elif language == "japanese":
        lng.channel_language[str(message.guild.id)] = 'ja-JP'
        await message.send(content=lng.tl("voice.set_language", str(message.guild.id)))
        lng.save_server_language()
    else:
        await message.send(content=lng.tl("no.lang", str(message.guild.id)).format(language))

@client.event
async def on_ready():
    print('봇시작')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/명령어")) #상태설정
    discord.Permissions.use_slash_commands = True

client.run(token)