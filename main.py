import discord  #import discord.py
import os  # gae ngambil barang dr environment
import random  # random nums gennerator
import youtube_dl #dl youtube vids
import asyncio
import pytz
from datetime import datetime, time, timedelta
from discord.ext import commands,tasks


# Variables/ Properties
genshin_asia = [
    421695374772797441, 876677366611587072, 431828098695036954,
    415861643524833290
]
genshin_na = [327494931105185792]
author_id_Hogan = 421695374772797441
author_id_ricad = 876677366611587072
author_id_aljosh = 415861643524833290
author_id_lie = 327494931105185792
diceNums = [1, 2, 3, 4, 5, 6]
hololiveMembers = [
    'Tokino Sora', 'Roboco', 'Sakura Miko', 'Hoshimachi Suisei', 'AZKi',
    'Yozora Mel', 'Shirakami Fubuki', 'Natsuiro Matsuri', 'Akai Haato',
    'Aki Rosenthal', 'Minato Aqua', 'Murasaki Shion', 'Nakiri Ayame',
    'Yuzuki Choco', 'Oozora Subaru', 'Ookami Mio', 'Nekomata Okayu',
    'Inugami Korone', 'Usada Pekora', 'Shiranui Flare', 'Shirogane Noel',
    'Houshou Marine', 'Uruha Rushia', 'Amane Kanata', 'Tsunomaki Watame',
    'Tokoyami Towa', 'Himemori Luna', 'Kiryu Coco', 'Yukihana Lamy',
    'Momosuzu Nene', 'Shishiro Botan', 'Omaru Polka', 'Mano Aloe',
    'La+ Darkness', 'Takane Lui', 'Hakui Koyori', 'Sakamata Chloe',
    'Kazama Iroha', 'Mori Calliope', 'Takanashi Kiara', "Ninomae Ina'nis",
    'Gawr Gura', 'Watson Amelia', 'IRyS', 'Tsukumo Sana', 'Ceres Fauna',
    'Ouro Kronii', 'Nanashi Mumei', 'Hakoz Baelz'
]
UTC = pytz.utc
IDP = pytz.timezone('America/Indiana/Indianapolis')
LA = pytz.timezone('America/Los_Angeles')
SBY = pytz.timezone('Asia/Jakarta')
globalResetTime = time(3, 0)
now = datetime.now()
asiaNow = datetime.now(SBY).replace(tzinfo=None, microsecond=0)
NANow = datetime.now(LA).replace(tzinfo=None, microsecond=0)
todayDate = now.date()
asiaDate = asiaNow.date()
NADate = NANow.date()
#AsiaResetToday = datetime.combine(todayDate, AsiaResetTime)
#NAResetToday = datetime.combine(todayDate, NAResetTime)
AsiaResetToday = datetime.combine(asiaDate,
                                  globalResetTime) + timedelta(days=1)
NAResetToday = datetime.combine(NADate, globalResetTime) + timedelta(days=1)
AsiaResetTimer = AsiaResetToday - asiaNow
NAResetTimer = NAResetToday - NANow
asiaStr = str(AsiaResetTimer)
NAStr = str(NAResetTimer)

#youtube_dl configs \/
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
#youtube_dl end config ^


bot = commands.Bot(command_prefix='$')
client = discord.Client()


@bot.command()
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        #await channel.disconnect() #testing purposes
    else:
        await ctx.send(
            "I am terribly sorry, but I cannot join you as you are not in a voice channel."
        )


@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def anya(ctx,url="https://www.youtube.com/watch?v=s5GLU4xZDgo&ab_channel=Animeiko"):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        #await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")
  

#lek bot e tangi
@bot.event
async def on_ready():
    otities = bot.get_channel(999239717155512342)
    print('Good Morning MF!!! - {0.user}'.format(bot))
    await otities.send('Bot is Online!')


@bot.command()
async def hello(ctx):
    await ctx.channel.send('Sup Bitj :3 ' + ctx.message.author.mention)


@bot.command()
async def hw(ctx):
    chosenHololiveWaifu = random.randrange(0, len(hololiveMembers), 1)
    await ctx.message.channel.send('Your waifu is ' +
                                   hololiveMembers[chosenHololiveWaifu])


@bot.command()
async def rt(ctx):
    if (ctx.author.id) in genshin_asia:
        await ctx.channel.send('Asia server will reset in ' +
                               str(AsiaResetTimer))
    elif (ctx.author.id) in genshin_na:
        await ctx.channel.send('NA server will reset in ' + str(NAResetTimer))


bot.run(os.getenv('TOKEN'))

# lek ngirim message
"""
@bot.event
async def on_message(message):
    # make all messages lower case
    lowerCaseMsg = message.content.lower()

    # supaya bot e ga baca msg ne dw
    if message.author == client.user:
        return
    # baca string tertentu
    if message.content.startswith('$hello'):
        await message.channel.send('Sup Bitj :3')
    if message.content.startswith('$aqua'):
        await message.channel.send('https://imgur.com/Kj7QIfl')

    # roll a dice
    if message.content.startswith('$roll'):
        chosenNum = random.choice(diceNums)
        await message.channel.send('You rolled> ' + str(chosenNum))

    # random waifu picker
    if (lowerCaseMsg.startswith('$hololiveWaifu')
            or lowerCaseMsg.startswith('$hw')):
        chosenHololiveWaifu = random.randrange(0, len(hololiveMembers), 1)
        await message.channel.send('Your waifu is ' +
                                   hololiveMembers[chosenHololiveWaifu])

    # timezones
    # show local time based on user id
    if (lowerCaseMsg.startswith('$mytime') or lowerCaseMsg.startswith('$mt')):
        if (message.author.id) == author_id_Hogan:
            await message.channel.send(('Hogan ') + str(datetime.now(SBY)))
        if (message.author.id) == author_id_ricad:
            await message.channel.send(('ricad ') + datetime.now(SBY).ctime())
        if (message.author.id) == author_id_aljosh:
            await message.channel.send(('aljos ') + datetime.now(IDP).ctime())
        #await message.channel.send('ISO FORMAT')
        #await message.channel.send('current time(UTC time test)> ' + datetime.now(UTC).isoformat())
        #await message.channel.send('current time(aljosh)> ' + datetime.now(IDP).isoformat())
        #await message.channel.send('current time(hoganRicad)> ' + datetime.now(SBY).isoformat())
        #await message.channel.send('CTIME')
        #await message.channel.send('current time(UTC time test)> ' + datetime.now(UTC).ctime())
        #await message.channel.send('current time(aljosh)> ' + datetime.now(IDP).ctime())
        #await message.channel.send('current time(hoganRicad)> ' + datetime.now(SBY).ctime())

    # show 'all' time zones
    if (lowerCaseMsg.startswith('$alltime') or lowerCaseMsg.startswith('$at')):
        await message.channel.send('current time(UTC)> ' +
                                   datetime.now(UTC).ctime())
        await message.channel.send('current time(aljosh)> ' +
                                   datetime.now(IDP).ctime())
        await message.channel.send('current time(lie)> ' +
                                   datetime.now(LA).ctime())
        await message.channel.send('current time(hoganRicad)> ' +
                                   datetime.now(SBY).ctime())

    # calculates genshin reset time
    if (lowerCaseMsg.startswith('$resettime')
            or lowerCaseMsg.startswith('$rt')):
        if (message.author.id) in genshin_asia:
            await message.channel.send('Asia server will reset in ' +
                                       str(AsiaResetTimer))
        elif (message.author.id) in genshin_na:
            await message.channel.send('NA server will reset in ' +
                                       str(NAResetTimer))

    # join voice channel
    if (lowerCaseMsg.startswith('$joinVc') or lowerCaseMsg.startswith('$jvc')):
        channel = message.author.voice.channel
        await channel.connect()


# run the bot
client.run(os.getenv('TOKEN'))
"""
