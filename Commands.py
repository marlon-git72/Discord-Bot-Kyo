import json
import random
from webbrowser import get
from discord.ext.commands import cooldown
from discord.utils import get
import aiohttp
import discord
from discord import Guild, Message, TextChannel, FFmpegPCMAudio, guild
from discord.ext import commands
import datetime
import asyncio
from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix='#')
bot.remove_command('help')

admin = 471336325543493655

client = discord.Client()


@bot.command()
async def stop(ctx):
    if ctx.author.id == admin:
        await bot.logout()







@bot.command()
async def userinfo(ctx, member : discord.Member):
    embed = discord.Embed(title=f'Userinfo für {member.name}#{member.discriminator}',
                          description="Das ist eine Userinfo für den User {}".format(member.mention),
                          color=member.color, timestamp=datetime.datetime.now())
    embed.add_field(name="Server beigetreten", value=member.joined_at.strftime("%d/%m/%Y, %H/%M:%S"),
                    inline=True)
    embed.add_field(name="Discord beigetreten", value=member.created_at.strftime("%d/%m/%Y, %H/%M:%S"),
                    inline=True)
    if member.bot:
        embed.add_field(name="Bot", value="✅", inline=False)
    else:
        embed.add_field(name="Bot", value="❌", inline=False)
        rollen = ""
        for role in member.roles:
            if not role.is_default():
                rollen += "{} \r\n".format(role.mention)
        if rollen:
            embed.add_field(name="Rollen", value=rollen, inline=False)
            embed.add_field(name='Aktueller Server', value=f"{member.guild}")
            embed.add_field(name='Höchste Rolle', value=f"{member.top_role}")
            embed.set_thumbnail(url=member.avatar_url)
            mess = await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=False, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Der User {member.mention} wurde wegen {reason} gemuted!")
    await member.send(
        f"Du wurdest in dem Server {guild.name} wegen {reason} gemuted!"
    )

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"{member.mention} wurde endmuted")
    await member.send("Du wurdest endmuted")




@bot.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        await member.kick(reason=reason)
        embed = discord.Embed(title="Erfolg✅", description=f"Der User {member.name} wurde vom Server gekickt!", color=0x22a7f0, timestamp=datetime.datetime.now())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Misserfolg❌", description=f"Der User {member.name} konnte nicht gekickt werden, da du nicht über die benötigten Rechte verfügst!",
                              color=0x22a7f0, timestamp=datetime.datetime.now())
        await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    if ctx.author.guild_permissions.ban_members:
        await member.ban(reason=reason)
        embed = discord.Embed(title="Erfolg✅", description=f"Der User {member.name} wurde vom Server gebannt!",
                              color=0x22a7f0, timestamp=datetime.datetime.now())
        embed.set_image(url="https://cdn.discordapp.com/attachments/739141186438168586/788807580583329823/tenor.gif")
        mess = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await mess.delete()
    else:
        embed = discord.Embed(title="Misserfolg❌",
                              description=f"Der User {member.name} konnte nicht gebannt werden, da du nicht über die benötigten Rechte verfügst!",
                              color=0x22a7f0, timestamp=datetime.datetime.now())
        await ctx.send(embed=embed)



@bot.event
async def on_ready():
    print("Eingeloogt als Kyo")

""""
@bot.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)


"""
with open('servers.json', encoding='utf-8') as f:
    servers = json.load(f)

    servers = {"servers": []}
    with open('servers.json', 'w') as f:
        json.dump(servers, f, indent=4)


@bot.command()
async def addGlobal(ctx):
    if ctx.author.guild_permissions.administrator:
        if not guild_exists(ctx.guild.id):
            server = {
                "guildid": ctx.guild.id,
                "channelid": ctx.channel.id,
                "invite": f'{(await ctx.channel.create_invite()).url}'
            }
            servers["servers"].append(server)
            with open('servers.json', 'w') as f:
                json.dump(servers, f, indent=4)
            await ctx.send('Globalchat wurde erfolgreich Erstellt✅.')


@bot.command()
async def removeGlobal(ctx):
    if ctx.member.guild_permissions.administrator:
        if guild_exists(ctx.guild.id):
            globalid = get_globalChat_id(ctx.guild.id)
            if globalid != -1:
                servers["servers"].pop(globalid)
                with open('servers.json', 'w') as f:
                    json.dump(servers, f, indent=4)
            await ctx.send('Entfernt.')


#########################################

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content.startswith('#'):
        if get_globalChat(message.guild.id, message.channel.id):
            await sendAll(message)
    await bot.process_commands(message)


#########################################

async def sendAll(message: Message):
    embed = discord.Embed(description=f"{message.content}", color=0x22a7f0)
    embed.set_footer(text='Gesendet von Server {}'.format(message.guild.name))
    embed.set_author(name=f"{message.author.name}#{message.author.discriminator}", icon_url=f"{message.author.avatar_url}")
    for server in servers["servers"]:
        guild: Guild = bot.get_guild(int(server["guildid"]))
        if guild:
            channel: TextChannel = guild.get_channel(int(server["channelid"]))
            if channel:
                await channel.send(embed=embed)
    await message.delete()


###############################

def guild_exists(guildid):
    for server in servers['servers']:
        if int(server['guildid'] == int(guildid)):
            return True
    return False



def get_globalChat(guild_id, channelid=None):
    globalChat = None
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            if channelid:
                if int(server["channelid"]) == int(channelid):
                    globalChat = server
            else:
                globalChat = server
    return globalChat


def get_globalChat_id(guild_id):
    globalChat = -1
    i = 0
    for server in servers["servers"]:
        if int(server["guildid"]) == int(guild_id):
            globalChat = i
        i += 1
    return globalChat




@bot.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    Region = str(ctx.guild.region)
    Member = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Informationen",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=Region, inline=True)
    embed.add_field(name="Member", value=Member, inline=True)

    await ctx.send(embed=embed)

###########################################################



@bot.command(aliases=['memes'])
async def meme(ctx):
    embed = discord.Embed(title="Meme", description=None)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/wholesomememes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed, content=None)





















"""
@bot.event
async def on_member_join(message):
    if message.author.id is not "users.json":
        with open('users.json', 'r') as f:
            user = {}
            user[str(message.author.id)] = {}
            user[str(message.author.id)]["level"] = 0
            user[str(message.author.id)]["exp"] = 0
            json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
    else:
        pass


@bot.event
async def update_data(users, message):
    if not f'{message.author.id}' in users:
        users[f'{message.author.id}']['exp'] = 0
        users[f'{message.author.id}']['level'] = 0

@bot.event
async def on_message(message):
    with open("users.json", "r", encoding="utf8") as f:
        user = json.load(f)
    try:]["level"]
                await message.channel.send(f"Oh, {message.author.name} ist aufgestiegen zu Level {lvl}")
                json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
                return
            json.dump(user, f, sort_keys=True, indent=4, ensure_asci
        with open("users.json","w",encoding="utf8") as f:
            user[str(message.author.id)]["exp"] = user[str(message.author.id)]["exp"]+1
            lvl_start = user[str(message.author.id)]["level"]
            lvl_end = user[str(message.author.id)]["exp"] ** (1.5/4)
            if lvl_start < lvl_end:
                user[str(message.author.id)]["level"] = user[str(message.author.id)]["level"] + 1
                lvl = user[str(message.author.id)i=False)
    except:
        with open("users.json","w",encoding="utf8") as f:
            user = {}
            user[str(message.author.id)] = {}
            user[str(message.author.id)]["level"] = 0
            user[str(message.author.id)]["exp"] = 0
            json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)


Status = "Wird gebaut... | #help"


@bot.command(pass_context=True)
async def play(ctx):
    if not ctx.message.author.voice:
        await ctx.send('you are not connected to a voice channel')
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice.client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player)

    await ctx.send(f'**Music:**{player.title}')
"""


@bot.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(bot.voice_clients, guild=ctx.guild)
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#words(1:)

@bot.command()
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{ctx.author.name}´s Finanzen⠀⠀⠀⠀⠀⠀⠀⠀⠀", color=0x22a7f0, timestamp=datetime.datetime.now())
    embed.add_field(name="Wallet", value=wallet_amt)
    embed.add_field(name="Bank", value=bank_amt)
    await ctx.send(embed=embed)


@bot.command()
async def seebalance(ctx, member: discord.Member):
    await open_account(member)
    user = member
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{member.display_name}´s Finanzen⠀⠀⠀⠀⠀⠀⠀⠀⠀", color=0x22a7f0, timestamp=datetime.datetime.now())
    embed.add_field(name="Wallet", value=wallet_amt)
    embed.add_field(name="Bank", value=bank_amt)
    embed.set_footer(text=f"Nachgefragt von {ctx.author.name}")
    await ctx.send(embed=embed)


@bot.command()
@cooldown(1, 60, commands.BucketType.user)
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)

    await ctx.send(f"Jemand hat dir {earnings} coins gegeben!")

    with open("mainbank.json", "r") as f:
        users = json.load(f)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)


@bot.command()
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Bitte lege einen Betrag fest")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("Du hast nicht genug Geld!")
        return
    if amount<0:
        await ctx.send("Der Betrag muss positiv sein!")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author,-1*amount, "bank")

    await ctx.send(f"Du hast {amount} coins ausgezahlt bekommen!")


@bot.command()
async def send(ctx, member: discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Bitte lege einen Betrag fest")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("Du hast nicht genug Geld!")
        return
    if amount<0:
        await ctx.send("Der Betrag muss positiv sein!")
        return


    await update_bank(ctx.author,-1*amount, "bank")
    await update_bank(member, amount, "bank")

    await ctx.send(f"Du hast {amount} coins an {member} abgegeben!")


@bot.command()
@cooldown(1, 6, commands.BucketType.user)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Bitte lege einen Betrag fest")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("Du hast nicht genug Geld!")
        return
    if amount < 0:
        await ctx.send("Der Betrag muss positiv sein!")
        return

    for i in range(3):
        a = random.choice(["4", "3", "3", "Ja", "Ja", "Ja", "Ja", "Nein", "Nein", "Nein", "Nein", "Nein", "Nein", "Nein", "Nein", "Nein", "Nein"])

    if a == "Ja":
        await update_bank(ctx.author,2*amount)
        await ctx.send("Du hast gewonnen und es verdoppelt!")
    if a == "3":
        await update_bank(ctx.author, 3 * amount)
        await ctx.send("Du hast gewonnen und es verdreifacht!")
    if a == "4":
        await update_bank(ctx.author, 4 * amount)
        await ctx.send("Du hast gewonnen und es vervierfacht!")
    if a == "Nein":
        await update_bank(ctx.author,-1* amount)
        await ctx.send("Du hast verloren!")







@bot.command()
async def deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Bitte lege einen Betrag fest")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("Du hast nicht genug Geld!")
        return
    if amount < 0:
        await ctx.send("Der Betrag muss positiv sein!")
        return




    await update_bank(ctx.author,-1*amount)
    await update_bank(ctx.author,amount, "bank")

    await ctx.send(f"Du hast {amount} coins eingezahlt!")


@bot.command()
async def depall(ctx):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author)

    amount = bal[0]

    if bal[0] == 0:
        await ctx.send("Du kannst 0 coins nicht einzahlen!")
        return
    else:
        await ctx.send(f"Du hast {amount} coins eingezahlt!")
        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")


@bot.command()
async def drawall(ctx):
    await open_account(ctx.author)

    bal = await update_bank(ctx.author)

    amount = bal[1]

    if bal[1] == 0:
        await ctx.send("Du kannst 0 coins nicht auszahlen!")
        return
    else:
        await ctx.send(f"Du hast {amount} coins ausgezahlt!")
        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")


strafe = -10000

@bot.command()
@cooldown(1, 14400, commands.BucketType.user)
async def rob(ctx, member: discord.Member):
    b = ["Ja", "Nein"]
    c = random.choice(b)
    if c == "Nein":
        await ctx.send("Oh nein! Du wurdest erwischt und musst Strafe zahlen!(10000 coins)")
        await update_bank(ctx.author, strafe)
        return
    else:
        await open_account(ctx.author)
        await open_account(member)

    bal = await update_bank(member)

    if bal[0]<100:
        await ctx.send("Das ist es nicht wert")
        return

    earnings = random.randrange(0, bal[0])

    await update_bank(ctx.author, earnings)
    await update_bank(member,-1*earnings)

    await ctx.send(f"Du hast {earnings} coins erbeutet")


@bot.command()
@cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = 100

    await ctx.send(f"Du hast deine Tägliche Belohnung von {earnings} coins abgeholt!!!")

    with open("mainbank.json", "r") as f:
        users = json.load(f)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)

@bot.command()
@cooldown(1, 604800, commands.BucketType.user)
async def weekly(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = 1000

    await ctx.send(f"Du hast deine Wöchentliche Belohnung von {earnings} coins abgeholt!!!")

    with open("mainbank.json", "r") as f:
        users = json.load(f)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users,f)


#604.800



async def open_account(user):

    users = await get_bank_data()

    with open("mainbank.json", "r") as f:
        users = json.load(f)

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users,f)


    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]

    return bal





bot.run(TOKEN)
