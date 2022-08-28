from discord import Intents
from discord.ext import commands
from discord import Activity
from discord import Status
from discord import app_commands
import dotenv, os


try:
    dotenv.load_dotenv("./token.env")
    token = os.getenv('token')
except:
    token = os.environ['token']


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=Intents.default(),
            sync_command=True,
            application_id=980368790032363571 #ㅁㄹ
        )
        self.initial_extension = [
            'cogs.register_channel_school',
            'cogs.select_test',
            'cogs.button_test'
        ]

    async def on_ready(self):
        print("login")
        await self.change_presence(status=Status.online, activity=Activity(name="학교 정보", type=3))

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await bot.tree.sync()


bot = Bot()
bot.run(token)