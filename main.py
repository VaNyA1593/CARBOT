
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from model import get_class

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def photo(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments:
            if attachment.filename.endswith('.jpg') or \
            attachment.filename.endswith('.jpeg') or \
            attachment.filename.endswith('.png'):
                image_path = f'./images/{attachment.filename}'
                await attachment.save(image_path)
                temp_msg = await ctx.send("Идёт обработка изображения...")
                class_name, probability = get_class(image_path, 'keras_model.h5', 'labels.txt')
                await temp_msg.delete()
                await ctx.send(f'С вероятностью {probability}% На картинке {class_name}')
                os.remove(image_path)
            else:
                await ctx.send("Можно только файлы .png .jpg .jpeg")
                return
    else:
        await ctx.send("Ой кажеться ты не отправил фото вместе с командой")

bot.run(DISCORD_TOKEN)