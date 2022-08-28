from discord import app_commands, Interaction
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle


class button_test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="버튼")
    async def button_test(self, interaction: Interaction) -> None:
        button1 = Button(label="버튼1", style=ButtonStyle.primary)

        async def button1_callback(interaction: Interaction):
            await interaction.response.send_message("1번입니다.")

        button1.callback = button1_callback
        view = View()
        view.add_item(button1)
        await interaction.response.send_message("버튼을 선택해주세요.", view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(button_test(bot))