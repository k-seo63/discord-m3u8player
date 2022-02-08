import discord
from discord.ext import tasks
from datetime import datetime


# Bot token
TOKEN: str = '' 

# Voicechannel ID
VCCHANNEL_ID: int = 

# URL of an .m3u8 file
API_URL = ''

# FFMPEG option for streaming 
FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 8',
        'options': '-vn'
        }

client = discord.Client()
voice_channel = None
voice_client = None

# Runs when the bot is started.
@client.event
async def on_ready():
    global voice_channel
    voice_channel = client.get_channel(VCCHANNEL_ID) 

    # Start the loop of the function that connects to the VoiceChannel at the specified time.
    scheduled_radio.start()
    print('Success: Login')


# Respond to chat
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # !test
    if message.content == '!test':
        await message.channel.send('Hi')
        return

    # !play
    if message.content == "!play":
        global voice_client
        if voice_client is None:
            voice_client = await voice_channel.connect()
            source = discord.FFmpegPCMAudio(API_URL, **FFMPEG_OPTIONS)
            voice_client.play(source)

    # !leave
    if message.content == "!leave":
        if voice_client is not None:
            voice_client.stop()
            await voice_client.disconnect()
            voice_client = None


# Loop every 15 seconds
@tasks.loop(seconds=15)
async def scheduled_radio():
    # connect at 6:25
    if datetime.now().hour==6 and datetime.now().minute==25:
        global voice_client
        if voice_client is None:
            voice_client = await voice_channel.connect()
            source = discord.FFmpegPCMAudio(API_URL, **FFMPEG_OPTIONS)
            voice_client.play(source)

    # connect at 6:45
    if datetime.now().hour==6 and datetime.now().minute==45:
        if voice_client is not None:
            voice_client.stop()
            await voice_client.disconnect()
            voice_client = None


client.run(TOKEN)
