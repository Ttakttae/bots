"""서버별 플레이 담당"""

import asyncio
from music_bot.scripts.music_playlist import *
from music_bot.scripts.language import *
from discord import FFmpegPCMAudio
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

global time
time = {}

lng = Language()
lng.load_all_language()
lng.load_server_language()

class music_playing:
    def __init__(self):
        self.tasks = []

    async def after_playing(self, voice, voice_channel, channel, playlist, server_id):
        await asyncio.sleep(playlist[voice_channel]["list"][0]["length"])
        next_playlist(voice_channel)
        try:
            self.source = FFmpegPCMAudio(playlist[voice_channel]["list"][0]["audio_url"], **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
            voice.play(self.source)  # play the source
            await channel.send(lng.tl("voice.play", server_id).format(playlist[voice_channel]["list"][0]["video_title"]))
            if playlist[voice_channel]["list"][0]["length"] == 0:
                pass
            else:
                await self.create_task(voice, voice_channel, channel, playlist, server_id)
        except:
            pass

    async def create_task(self, voice, voice_channel, channel, playlist, server_id):
        """
        테스크를 만듦니다
        :param voice: obj
        :param voice_channel: channel_id
        :param channel: channel_obj
        :param playlist: dict
        :return: None
        """
        time[voice_channel] = {"now-remaining" : playlist[voice_channel]["list"][0]["length"], "paused-time" : 0}
        self.task1 = asyncio.create_task(self.after_playing(voice, voice_channel, channel, playlist, server_id))
        self.task2 = asyncio.create_task(self.counting(playlist[voice_channel]["list"][0]["length"], voice_channel))
        self.tasks.append(self.task1)
        self.tasks.append(self.task2)
        await self.task1
        await self.task2

    async def counting(self, second, voice_channel):
        self.seconds = second
        while not self.seconds == 0:
            self.seconds = self.seconds - 1
            time[voice_channel]["now-remaining"] = self.seconds
            await asyncio.sleep(1)

    async def task_kill(self):
        for self.ta in self.tasks:
            self.ta.cancel()
        self.__init__()