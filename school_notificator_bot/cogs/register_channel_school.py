from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord import Object


class register_channel_school(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="register_channel_school", description="bla bla bla")
    async def register_channel_school(self, interaction: Interaction) -> None:
        await interaction.response.send_message("hi")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(register_channel_school(bot))