import discord
from discord.ext import commands
import datetime
import wikipedia


client = commands.Bot(command_prefix = "#")

client.remove_command("help")

admin = 471336325543493655

@client.event
async def on_ready():
    time = datetime.datetime.now()
    print("Online")

def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=4, chars=1000, auto_suggest=True, redirect=True)
    return definition

@client.event
async def on_message(message):
    words = message.content.split()
    important_words = words[1:]





#words(1:)

    if message.content.startswith("#wiki"):
        words = message.content.split()
        important_words = words[1]
        search = discord.Embed(title=f"Suchergebnis zu: {important_words}", description=wiki_summary(important_words), color=0x22a7f0, timestamp=datetime.datetime.now())
        await message.channel.send(content=None, embed=search)


    if message.content.startswith("#stop"):
        if message.author.id == admin:
            await client.logout()




client.run(TOKEN)


