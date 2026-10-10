import discord
from discord.ext import commands
from discord import app_commands
from reader2 import *
from ghost_button import GhostView
import pandas as pd
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
#client = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.attachments:
        if str(message.attachments) == "[]": # Checks if there is an attachment on the message
            return
        else: # If there is it gets the filename from message.attachments
            split_v1 = str(message.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            if filename.endswith(".xlsx") or filename.endswith(".csv"):
                if filename.endswith(".xlsx"):
                    await message.attachments[0].save(fp="./{}".format(filename)) # saves the file
                    df = pd.read_excel(filename, sheet_name="Worksheet", engine="openpyxl")
                    df.to_csv(filename[:-5] + ".csv", index=False, encoding="utf-8")
                    filename = filename[:-5] + ".csv"
                elif filename.endswith(".csv"): # Checks if it is a .csv file
                    await message.attachments[0].save(fp="./{}".format(filename)) # saves the file

                if filename.startswith("report"):
                    template_write_spi(f"./{filename}")
                    bulk_poster_spi(f"./{filename}")
                elif filename.startswith("board-export"):
                    template_write(f"./{filename}")
                    bulk_poster(f"./{filename}")
                            
                with open("./daily_templates.txt", 'rb') as f:
                    picture = discord.File(f)
                    await message.channel.send(file=picture)
                    
                with open("./bulk_posting.csv", 'rb') as c:
                    picture = discord.File(c)
                    await message.channel.send(file=picture)
                
                view = GhostView()
                await message.channel.send("", view=view)


@bot.tree.command(name="ghostpost")
async def ghostpost(interaction):
    user_input = GhostPostModal()
    await interaction.response.send_modal(user_input)



bot.run(os.getenv("API_TOKEN"))
