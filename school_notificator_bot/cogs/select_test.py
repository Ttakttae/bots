from discord import app_commands
from discord.ext import commands
from discord import Interaction
from discord.ui import View, Select
from discord import SelectOption


class select_test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="select_test", description="test")
    async def select_test(self, interaction: Interaction) -> None:
        selects = Select(options=[
            SelectOption(
                label="1번",
                description="1번"
            ),
            SelectOption(
                label="2번",
                description="2번"
            )
        ])

        async def select_callback(interaction: interaction) -> None:
            await interaction.response.send_message(f"{selects.values[0]}를 선택하셨습니다.")

        selects.callback = select_callback
        view = View()
        view.add_item(selects)
        await interaction.response.send_message("메뉴를 선택해주세요.", view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(select_test(bot))