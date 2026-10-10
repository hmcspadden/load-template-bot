import discord
from discord import ui
from ghost_post import ghost_post

radius_options = [
        discord.SelectOption(label="25 miles", value = "25"),
        discord.SelectOption(label="50 miles", value = "50"),
        discord.SelectOption(label="100 miles", value = "100", default=True),
        discord.SelectOption(label="150 miles", value = "150"),
        discord.SelectOption(label="200 miles", value = "200")
]

quant_options = [
        discord.SelectOption(label="1", value = "1"),
        discord.SelectOption(label="2", value = "2"),
        discord.SelectOption(label="3", value = "3"),
        discord.SelectOption(label="4", value = "4"),
        discord.SelectOption(label="5", value = "5", default=True),
        discord.SelectOption(label="6", value = "6"),
        discord.SelectOption(label="7", value = "7"),
        discord.SelectOption(label="8", value = "8"),
        discord.SelectOption(label="9", value = "9"),
        discord.SelectOption(label="10", value = "10")
]


class GhostPostModal(discord.ui.Modal, title='Ghost Post'):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.origin_radius = self.add_item(ui.Label(
            text="Origin Radius", 
            component=ui.Select(
                placeholder="Origin Radius", 
                options=radius_options
            )
        ))

        self.destination_radius = self.add_item(ui.Label(
            text="Destination Radius",
            component=ui.Select(
                placeholder="Destination Radius", 
                options=radius_options
            )
        ))

        self.quantity = self.add_item(ui.Label(
            text="Number of Ghost Posts",
            component=ui.Select(
                placeholder="Number of Ghost Posts", 
                options=quant_options
            )
        ))
    
    async def on_submit(self, interaction):
        origin_radius = self.children[0].component.values[0]
        destination_radius = self.children[1].component.values[0]
        quantity = self.children[2].component.values[0]

        ghost_post(origin_radius, destination_radius, quantity)

        with open("./ghost_post.csv", 'rb') as c:
            picture = discord.File(c)
            await interaction.response.send_message(file=picture)
