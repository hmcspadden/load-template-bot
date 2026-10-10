import discord 
from ghost_post_modal import GhostPostModal

class GhostView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ghost Post", style=discord.ButtonStyle.primary, emoji="👻")
    async def button_callback(self, interaction, button):
        ghostpost = GhostPostModal()
        await interaction.response.send_modal(ghostpost)