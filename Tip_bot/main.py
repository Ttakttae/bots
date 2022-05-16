# TM. TTACTTAE

import discord
from scripts.assets import Assets
from scripts.emoji import Emoji


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())

        self.asset = Assets()
        self.emoji = Emoji()

    async def on_ready(self):
        print(f"KEY: {self.asset.key}")
        print("# READY #")
        return

    async def on_message(self, message):
        if message.author.bot: return

        if message.content[:1] == ">":
            command, *options = message.content[1:].split(" ")
            channel = message.channel
            author_id = message.author.id

            if author_id in self.asset.white_list:
                if command == "전송":
                    content = self.emoji.replace_text_to_emoji(" ".join(options))
                    await channel.send(content)
                    await message.delete()
                    return
        return

    def run(self):
        super().run(self.asset.key)


if __name__ == '__main__':
    Client().run()
