import discord
import asyncio
import random
from discord import User
import datetime
from time import sleep


client = discord.Client()



#admin
admin = 471336325543493655

admin2 = "-"

note = []


coinflip = ["Kopf", "Zahl"]

#Status

Status = "Wird gebaut... | #help"


Bad_Words = ["fuck", "Fuck", "FUCK", "FuCK", "f**k", "F**k", "F**K", "FUcK", "FucK", "FuCk", "fUcK", "fUCK", "fUcK", "fuk", "fuCK", "fUck", "FUcK", "fUCk"]

passwort = "MARLON/PY"

#ready+status-task
@client.event
async def on_ready():
    print("Ich bin eingeloggt als {}".format(client.user.name))
    await client.change_presence(activity=discord.Game(Status), status=discord.Status.online)





#check
def is_not_pinned(mess):
    return not mess.pinned

#commands
@client.event
async def on_message(message):
    global mess, voicechannel
    if message.author.bot:
        return
    if message.content.startswith("#clear"):
        if message.author.permissions_in(message.channel).manage_messages:
            await message.delete()
            args = message.content.split(" ")
            if len(args) == 2 and args[1].isdigit():
                count = int(args[1]) + 1
                deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                embed = discord.Embed(title="Erfolg✅ ",
                                      description="Du hast {} Nachrichten gelöscht".format(len(deleted) - 1),
                                      color=0x22a7f0, timestamp=datetime.datetime.now())
                mess = await message.channel.send(embed=embed)
                await asyncio.sleep(10)
                await mess.delete()
    if message.content.startswith('#unban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            user: User = discord.utils.find(lambda m: args[1] in m.user.name, await message.guild.bans()).user
            if user:
                embed = discord.Embed(title="Erfolg✅", description=f"Der User {user.name} wurde entbannt!",
                                      color=0x22a7f0, timestamp=datetime.datetime.now())
                await message.guild.unban(user)
                await message.channel.send(embed=embed)
    if message.content.startswith("#stop"):
        if message.author.id == admin:
            embed = discord.Embed(title="Erfolg✅",
                                  description=f"{client.user.name} wurde erfolgreich gestoppt und ausgeschaltet!",
                                  color=0x22a7f0, timestamp=datetime.datetime.now())
            await message.channel.send(embed=embed)
            await client.logout()
        else:
            embed = discord.Embed(title="Misserfolg❌",
                                  description="Da du nicht der Admin des Bots bist funktioniert dieser Befehl nicht!",
                                  color=0x22a7f0, timestamp=datetime.datetime.now())
            embed.set_image(url="https://i.pinimg.com/originals/e5/8c/df/e58cdfdc496b880c8ff721d441adbe08.gif")
            await message.channel.send(embed=embed)
    if message.content.startswith("#ping"):
        ping = round(client.latency * 1000)
        if ping >= 0 and ping <= 200:
            color = 0x22a7f0
        elif ping >= 200 and ping <= 500:
            color = 0xff8400
        elif ping >= 500:
            color = 0xff0000
        else:
            color = 0x22a7f0
            print(f"error! ping: {ping} data: {message.author.name} , {message.author.guild}")
            await message.channel.send("Ein fehler ist aufgetreten!\n\r"
                                       "Bitte versuche es später noch einmal!")
        embed = discord.Embed(title=f"PONG!", description=f"Mein Ping beträgt aktuell: **{ping}**ms", color=color,
                              timestamp=datetime.datetime.now())
        await message.channel.send(embed=embed)
    if message.content.startswith("#coinflip"):
        embed = discord.Embed(colour=0x22a7f0)
        embed.set_image(url="https://multipletradings.com/broker/images/slide02_02.gif")
        mess = await message.channel.send(embed=embed)
        await asyncio.sleep(2)
        await mess.delete()
        embed = discord.Embed(title="{}".format(random.choice(coinflip)), color=0x22a7f0)
        await message.channel.send(embed=embed)
    if message.content.startswith("#help"):
        embed = discord.Embed(title="**Hey! Wie kann ich dir helfen?**", color=0x22a7f0,
                              timestamp=datetime.datetime.now())
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/739141186438168586/788882564840292392/Bongo_Cat.png")
        embed.add_field(name="⚙**️Manage**", value=f"`ban`, `kick`, `clear`, `mute`, `unmute`", inline=False)
        embed.add_field(name="🕹**Fun**", value="`coinflip`, `qr/`, `meme`", inline=False)
        embed.add_field(name="🌎**Global-Chat**", value="`addGlobal`, `removeGlobal`", inline=False)
        embed.add_field(name="🎵**Musik**", value="`play`, `quit`", inline=False)
        embed.add_field(name="📖**Nützliches**", value="`userinfo`, `serverinfo`, `embed`, `wiki`", inline=False)
        embed.add_field(name="📈**Konto**", value="`balance`, `beg`, `withdraw`, `deposit`, `slots`, `seebalance`, `weekly`, `daily`, `depall`, `drawall`", inline=False)
        embed.add_field(name="**Smash-Turnier**", value="`turnier (Datum) (Uhrzeit) (Ping)`", inline=False)
        embed.add_field(name="👀**Kyo**", value="`about`, `ping`, `status`, `stop`", inline=False)
        embed.add_field(name="⠀⠀⠀",
                        value=f"[invite](https://discord.com/oauth2/authorize?client_id=765304469461663814&scope=bot&permissions=8) | [Server](https://discord.gg/Pyv2j7QTaD) | [Website](http://zmdevs.sytes.net/)",
                        inline=False)
        embed.set_footer(text=f"Prefix = >#<  |  nachgefragt von: {message.author.name}")
        await message.channel.send(embed=embed)
    if message.content.startswith("#embed"):
        args = message.content.split(" ")
        if len(args) >= 3:
            description = " ".join(args[2:])
            embed = discord.Embed(title=f"{args[1]}", description=f"{description}", color=0x22a7f0,
                                  timestamp=datetime.datetime.now())
            embed.set_footer(text=f"Embed von {message.author.name}")
            await message.channel.send(embed=embed)
    if message.content.startswith("#about"):
        embed = discord.Embed(title="**Du willst also etwas über mich wissen...**", color=0x22a7f0,
                              timestamp=datetime.datetime.now())
        embed.add_field(name="⠀⠀⠀",
                        value=f"[invite](https://discord.com/oauth2/authorize?client_id=765304469461663814&scope=bot&permissions=8)",
                        inline=False)
        await message.channel.send(embed=embed)
    if message.content.startswith("#turnier"):
        if message.author.id == "658323094087401472" or "536161180474015746":
            await message.delete()
            args = message.content.split(" ")
            if len(args) >= 4:
                embed = discord.Embed(title="**Ein neues Smash Turnier!**",
                                  description=f"Ein neues Smash Turnier steht an! Es findet am **{args[1]}** um **{args[2]}** statt. Falls ihr euch anmelden wollt oder Fragen habt, meldet euch bei **Robin** oder **BotwLeon**. Und damit ihr es mitbekommt ein kleines {args[3]}",
                                  color=0x22a7f0, timestamp=datetime.datetime.now())
                await message.channel.send(embed=embed)
    if message.content.startswith("#status"):
        if message.author.id == admin:
            args = message.content.split("/")
            await message.channel.send(f"Status erfolgreich zu `{args[1]}` geändert")
            await client.change_presence(activity=discord.Game(args[1]), status=discord.Status.online)
        else:
            embed = discord.Embed(title="**Fehler**❌", description="Du bist nicht der Bot Admin", color=0x22a7f0)
            await message.channel.send(embed=embed)
    if message.content in Bad_Words:
        await message.delete()
    if message.content.startswith("#qr"):
        args = message.content.split('/')
        await message.channel.send(f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={args[1]}")
    if message.content.startswith("#note"):
        if message.author.id == admin:
            args = message.content.split("/")
            note.append(args[1])
            print("Note wurde hinzugefügt")
            mess = await message.channel.send("Notiz hinzugefügt!")
            await message.delete()
    if message.content.startswith("#seenote"):
        if message.author.id == admin:
            print(note)
            embed = discord.Embed(title="**Notizen**", description=f"{note}", color=0x22a7f0, timestamp=datetime.datetime.now())
            mess = await message.channel.send(embed=embed)
    if message.content.startswith("#delnote"):
        if message.author.id == admin:
            note.pop()
            await message.channel.send("letzte Notiz gelöscht!")
            print("Letzte Notiz gelöscht!")
            print(note)
    if message.content.startswith("#global.py"):
        await message.author.send("Passwort:")
    if message.content.lower() == "marlon/py" and str(message.channel.type) == "private":
        embed = discord.Embed(title="**Global-Chatbot**", description="Test", color=0x22a7f0, timestamp=datetime.datetime.now())
        await message.author.send(embed=embed)
        str(args[1])





#default = 0
  #  teal = 0x1abc9c
  #  dark_teal = 0x11806a
   # green = 0x2ecc71
   # dark_green = 0x1f8b4c
   # blue = 0x3498db
   # dark_blue = 0x206694
  #  purple = 0x9b59b6
  #  dark_purple = 0x71368a
   # magenta = 0xe91e63
   # dark_magenta = 0xad1457
   # gold = 0xf1c40f
  #  dark_gold = 0xc27c0e
  #  orange = 0xe67e22
  #  dark_orange = 0xa84300
  #  red = 0xe74c3c
   # dark_red = 0x992d22
  #  lighter_grey = 0x95a5a6
 #   dark_grey = 0x607d8b
  #  light_grey = 0x979c9f
  #  darker_grey = 0x546e7a
  #  blurple = 0x7289da
  #  greyple = 0x99aab5



client.run(TOKEN)
