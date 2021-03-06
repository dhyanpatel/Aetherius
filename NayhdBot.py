import discord, asyncio, logging
import mobcrush, gamelocker
import pickle
import pyowm
import requests, json, bs4
from discord.ext import commands
from random import randint
from music import Music,VoiceEntry,VoiceState
from cleverwrap import CleverWrap
from apiclient.discovery import build
from ctypes.util import find_library
from apiclient.errors import HttpError
from discord.ext.commands.errors import CommandNotFound
from poll import Poll
from recruitment import Recruitment
from toxic import Toxic
import time


owm = pyowm.OWM('Removed for Obvious Reasons')
cw = CleverWrap('Removed for Obvious Reasons')
bot = commands.Bot(command_prefix='+', description='Aetherius')
bot.add_cog(Music(bot))
bot.add_cog(Poll(bot))
bot.add_cog(Recruitment(bot))
bot.add_cog(Toxic(bot))
yt_api_key = 'Removed for Obvious Reasons'
service = build('youtube', 'v3', developerKey=yt_api_key)
chatChannels = {}




def search_videos(query, max_results=1):
    search = service.search().list(
        q=query,
        part="id,snippet",
        maxResults=max_results
    ).execute()
    return search

def box(arraylist):
    final = "```\n"
    for element in arraylist:
        final += element
    final += '\n```'
    return final

def get_xkcd_num():
    url = 'https://c.xkcd.com/random/comic/'
    response = requests.get(url)
    return int(response.url[17:][:-1])

#Gets Random Image Link
def get_xkcd_url(maxnum):
    url = 'https://xkcd.com/{}/info.0.json'.format(randint(0,maxnum))
    data = requests.get(url)
    json_data = data.text
    data = json.loads(json_data)
    return data['img']

def get_cat_link(num):
    url = 'http://thecatapi.com/api/images/get'
    parameters = {
        'api_key': 'Removed for Obvious Reasons',
        'format': 'html',
        'type': 'png',
        'results_per_page': str(num)
    }
    response = requests.get(url, params=parameters)
    html = response.content
    soup = bs4.BeautifulSoup(html, 'html.parser')
    list = []
    for link in soup.find_all('img'):
        list.append((link.get('src')))
    
    return list

def get_youtube_vid_link(search):
    data = search_videos(search)
    videoID = data['items'][0]['id']['videoId']
    youtubeLink = 'https://www.youtube.com/watch?v={}'.format(videoID)
    return youtubeLink


@bot.command(pass_context = True)
async def weather(ctx, *, place : str):
    """Returns weather in area based off Search Terms.
    Made thanks to OWM and PyOWM"""
    try:
        observation = owm.weather_at_place(place)
        location, weather = observation.get_location().get_name() , observation.get_weather()
        wind, humidity, heat = weather.get_wind() , weather.get_humidity() , weather.get_temperature('fahrenheit')
        link = 'https://openweathermap.org/city/{}'.format(observation.get_location().get_ID())
        embedded = discord.Embed(color = discord.Color.gold())
        embedded.set_author(
            url = link,
            name = 'Weather in {}'.format(location)
        )
        embedded.add_field(
            name = 'Wind Speed',
            value = '{} m/s'.format(wind['speed']),
            inline = True
        )
        embedded.add_field(
            name = 'Humidity',
            value = '{}%'.format(humidity),
            inline = True
        )
        embedded.add_field(
            name = 'Temperature',
            value = '{}°F'.format(heat['temp']),
            inline = True
        )

        await bot.say(embed = embedded)
    except Exception:
        await bot.say("Fuck you, that's not a place")

@bot.command(pass_context = True, aliases = ['Ping'])
async def ping(ctx):
    """Pings the Discord servers and returns the response time."""
    await bot.send_typing(ctx.message.channel)
    startTime = time.monotonic()
    await (await bot.ws.ping())
    endTime = time.monotonic()
    ping = (endTime - startTime) * 1000
    await bot.say('The server response time was {}ms'.format(int(ping)))


@bot.command(pass_context = True, aliases = ['Clever','cleverbot','Cleverbot'])
async def clever(ctx, *, input: str):
    """Accesses the CleverbotAPI and let's the user talk to Cleverbot.
    Made thanks to Cleverbot and Cleverwrap"""
    await bot.send_typing(ctx.message.channel)
    embedded = discord.Embed(title = cw.say(input), color = discord.Color.gold())
    await bot.say(embed = embedded)

@bot.command(pass_context = True)
async def urban(ctx, *, input: str):
    """Accesses the Urban Dictionary API and returns the definition of the user's search.
    Made thanks to Urban Dictionary"""
    try:
        url = 'https://mashape-community-urban-dictionary.p.mashape.com/define'
        parameters = {
            'term':input
        }
        headers = {
            "X-Mashape-Key": "Removed for Obvious Reasons",
            "Accept": "text/plain"
        }
        response = requests.get(url, params=parameters, headers = headers)
        json = response.json()

        embedded = discord.Embed(
            title = json['list'][0]['word'],
            url = json['list'][0]['permalink'],
            color = discord.Color.gold()
        )
        #embedded.set_author()
        embedded.add_field(
            name = 'Definition',
            value = json['list'][0]['definition'],
            inline = True
        )
        embedded.add_field(
            name = 'Example',
            value = json['list'][0]['example'],
            inline = True
        )
        embedded.add_field(
            name = 'Author',
            value = json['list'][0]['author'],
            inline = True
        )
        await bot.say(embed = embedded)
    except(IndexError):
        await bot.say('That\'s not a word in Urban Dictionary')


@bot.command(pass_context = True, aliases = ['Youtube','you','You'])
async def youtube(ctx, *, search : str = 'https://www.youtube.com/watch?v=id45kDNdXzA'):
    """Uses the YoutubeAPI to return the Video/Playlist/Channel of the user's search.
    Get's the first result of the search.
    Made thanks to YoutubeAPI and their wrapper"""
    try:
        await bot.send_typing(ctx.message.channel)
        youtubeLink = get_youtube_vid_link(search)
        await bot.say(youtubeLink)
    except(KeyError):
        try:
            await bot.send_typing(ctx.message.channel)
            data = search_videos(search)
            channelID = data['items'][0]['id']['channelId']
            youtubeLink = 'https://www.youtube.com/channel/{}'.format(channelID)
            await bot.say(youtubeLink)
        except(KeyError):
            try:
                await bot.send_typing(ctx.message.channel)
                data = search_videos(search)
                playlistID = data['items'][0]['id']['playlistId']
                youtubeLink = 'https://www.youtube.com/playlist?list={}'.format(playlistID)
                await bot.say(youtubeLink)
            except Exception:
                await bot.say("Sorry, something went wrong.")

@bot.command(pass_context = True)
async def lfg(ctx):
    """Specifically for The Legendary HQ guild.
    Allows users to find people to play with."""
    message = '{}, {} is looking for a party!'.format('<@&321091617245233154>', ctx.message.author.mention)
    await bot.say(message)

@bot.command(pass_context = True, aliases = ['Clear','wipe','Wipe'])
async def clear(ctx, number : int = 0):
    """Clears the chat channel based off how the number the user inputs.
    Defaults to 0 clears unless a number is specified.
    """
    try:
        clearlist = open('clearlist.txt', 'r').read().splitlines()
        if ctx.message.author.id in clearlist:
            pass
        else:
            await bot.send_typing(ctx.message.channel)
            await bot.say("You're not authorized")
            return

        deleted = await bot.purge_from(ctx.message.channel, limit = number+1)
        await bot.say('{} has cleared {} messages'.format(ctx.message.author, number))
        #await bot.send_message(ctx.message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    except Exception as e:
        print(e)
        deleted = await bot.purge_from(ctx.message.channel, limit=1)
        await bot.send_message(ctx.message.channel, "Can't delete messages older than 14 days.")


@bot.command(pass_context = True, aliases = ['mobcrush','Mob','Mobcrush'])
async def mob(ctx, name: str = 'mobcrush'):
    """Gets info about Mobcrush streamers
    Made thanks to the Mobcrush wrapper."""
    # Finds info about a streamer
    try:
        await bot.send_typing(ctx.message.channel)
        streamer = mobcrush.streamer(name)
        profileurl = "https://www.mobcrush.com/{}".format(streamer.name)
        embedded = discord.Embed(description=streamer.description, color=discord.Color.gold())
        embedded.set_thumbnail(url=streamer.lastbroadcast.snapshot)
        if (streamer.profilepic != None):
            embedded.set_author(name=streamer.name, url=profileurl, icon_url=streamer.profilepic)
        if streamer.islive == True:
            embedded.title = '🔴'
        elif streamer.islive == False:
            embedded.title = '⭕️'
        embedded.add_field(name="Followers", value=streamer.followercount, inline=True)
        embedded.add_field(name="Broadcasts", value=streamer.broadcastcount, inline=True)
        embedded.set_footer(text="Thanks to SEMC and Mobcrush")
        await bot.say('Getting streamer info...', embed=embedded)
    except Exception as e:
        await bot.send_typing(ctx.message.channel)
        print(e)
        await bot.say('This streamer wont work for some reason or the other.')


@bot.command(pass_context = True, aliases = ['Channelinfo','channel','Channel'])
async def channelinfo(ctx):
    """Gets info about the Discord channel"""
    try:
        await bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.gold())
        embedded.add_field(
            name = 'Server',
            value = ctx.message.channel.server,
            inline = True
        )
        embedded.add_field(
            name = 'Channel Name',
            value = ctx.message.channel.name,
            inline = True
        )
        embedded.add_field(
            name = 'Channel ID',
            value = ctx.message.channel.id,
            inline = True
        )

        await bot.say(embed = embedded)
    except Exception as e:
        print(e)


@bot.command(pass_context = True, aliases = ['Mobrecent','Mobcrushrecent','mobcrushrecent'])
async def mobrecent(ctx, name: str = 'mobcrush'):
    """Gets info about specified Mobcrush streamers' most recent streams
    Made thanks to Mobcrush wrapper"""
    try:
        await bot.send_typing(ctx.message.channel)
        streamer = mobcrush.streamer(name)
        broadcast = streamer.lastbroadcast
        profileurl = "https://www.mobcrush.com/{}".format(streamer.url)
        embedded = discord.Embed(title=streamer.name, description=broadcast.title, color=discord.Color.gold(),
                                 url=profileurl)
        embedded.add_field(name="Game", value=broadcast.game.name)
        embedded.add_field(name="Likes", value=broadcast.likes, inline=False)
        embedded.add_field(name="Views", value=broadcast.views, inline=False)
        embedded.set_thumbnail(url=broadcast.snapshot)

        await bot.say('Getting Broadcast Info...', embed=embedded)
    except Exception as e:
        await bot.send_typing(ctx.message.channel)
        print(e)
        await bot.say('')


@bot.command(pass_context = True, aliases = ['Say', 'repeat','Repeat'])
async def say(ctx, *, usertext : str):
    """Repeats what the user said."""
    if ctx.message.author.id == '282606266663305236': #Makes sure bot doesn't respond to itself
        return
    else:
        await bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color=discord.Color.gold())
        embedded.add_field(
            name = ctx.message.author.display_name,
            value = usertext,
            inline = True
        )
        await bot.say(embed = embedded)

@bot.command(pass_context = True)
async def adminsay(ctx, *,usertext : str):
    """For admins. Repeats user's input without an Embed"""
    adminlist = open('adminlist.txt','r').read().splitlines()
    try:
        await bot.send_typing(ctx.message.channel)
        if ctx.message.author.id in adminlist:
            if str(ctx.message.channel) != "general":
                deleted = await bot.purge_from(ctx.message.channel, limit = 1)
                await bot.say(usertext)
            else:
                deleted = await bot.purge_from(ctx.message.channel, limit=1)
                await bot.say(usertext)
    except Exception as e:
        print(e)


@bot.command(pass_context = True, aliases = ['Rate'])
async def rate(ctx, *, usertext : str = 'NayhdBot'):
    """Generates a random number to \"rate\" something"""
    await bot.send_typing(ctx.message.channel)
    if usertext == 'NayhdBot':
        embedded = discord.Embed(color=discord.Color.gold())
        embedded.add_field(
            name='∞',
            value=":thinking: | **{0}**, I\'d give {1} a {2}/10".format(ctx.message.author.display_name, usertext,
                                                                        '∞'),
            inline=False
        )
        await bot.say(embed=embedded)
    else:
        await bot.send_typing(ctx.message.channel)
        rating = randint(0,10)
        embedded = discord.Embed(color = discord.Color.gold())
        embedded.add_field(
            name = rating,
            value = ":thinking: | **{0}**, I\'d give {1} a {2}/10".format(ctx.message.author.display_name, usertext, rating),
            inline = False
        )
        await bot.say(embed = embedded)


@bot.command(pass_context = True, aliases = ['XKCD','xckd','xdck','kxcd','kxdc'])
async def xkcd(ctx):
    """Gets a random xkcd comic"""
    await bot.send_typing(ctx.message.channel)
    await bot.say(get_xkcd_url(get_xkcd_num()))


@bot.command(pass_context = True, aliases = ['logout','logoff'])
async def shutdown(ctx):
    """Admin Only
    Shuts down the bot."""
    await bot.send_typing(ctx.message.channel)
    admins = open('adminlist.txt','r').read().splitlines()
    if ctx.message.author.id in admins:
        await bot.say("Logging Off")
        await bot.logout()
    else:
        await bot.say("You're not authorized to do this")


@bot.command(pass_context=True, aliases=['eric', 'cats', 'Cat', 'Eric'])
async def cat(ctx, num: int = 1):
    """Gets a random Cat picture.
    Made thanks to The Cat API"""
    await bot.send_typing(ctx.message.channel)
    adminlist = open('adminlist.txt', 'r').read().splitlines()
    if ctx.message.author.id in adminlist:
        urllist = get_cat_link(num)
        for link in urllist:
            await bot.say(link)
    else:
        if num <= 3:
            urllist = get_cat_link(num)
            for link in urllist:
                await bot.say(link)
        else:
            await bot.say('You\'re not authorized to do more than 3')
            num = 1
            urllist = get_cat_link(num)
            for link in urllist:
                await bot.say(link)

@bot.command(pass_context = True)
async def welcome(ctx):
    """Sets the default Welcome channel for new users to be welcomed in"""
    await bot.send_typing(ctx.message.channel)
    admins = open('adminlist.txt').read().splitlines()
    if ctx.message.author.id in admins:
        pass
    else:
        await bot.say("You're not authorized")
        return
    chatChannels[ctx.message.server] = ctx.message.channel
    await bot.say('Default Welcome Channel Set!')

@bot.command(pass_context = True)
async def spam(ctx, times : int = 1, *, statement : str = "Spam"):
    """Admins Only
    Spam's the user's message for <int> times."""
    adminlist = open('adminlist.txt').read().splitlines()
    if ctx.message.author.id in adminlist:
        for step in range(times):
            await bot.send_typing(ctx.message.channel)
            await bot.say(statement)
    else:
        await bot.send_typing(ctx.message.channel)
        await bot.say('Yeah... No')

@bot.command(pass_context = True)
async def draft(ctx, ign : str = 'Aethen', region: str = 'na'):
    """Gets Vainglory draft info
    Doesn't work unless player's most recent match was a Ranked or Private Draft"""
    try:
        dpp_api_key = 'Removed for Obvious Reasons'
        try:
            api = gamelocker.Vainglory(dpp_api_key)
        except Exception as e:
            print('API Key Did not work')
        args = {'page[limit]': '1', 'filter[playerNames]': '{}'.format(ign), 'sort': '-createdAt'}
        data = api.matches(args, '{}'.format(region))
        #print(data)
        match_id = (data[0]['id'])
        data = api.match(match_id)

        telemetry_url = data[0]['telemetry']['URL']

        print(telemetry_url)
        response = requests.get(url=telemetry_url)

        progress = 0
        counter = 0
        final = '```'
        while progress < 8:
            try:
                if response.json()[counter]['type'] == 'HeroSkinSelect':
                    pass
                    counter += 1
                else:
                    if response.json()[counter]['type'] == 'HeroBan':
                        type = ' Banned '
                    elif response.json()[counter]['type'] == 'HeroSelect':
                        type = ' Selected '
                    team = response.json()[counter]['payload']['Team']
                    hero = response.json()[counter]['payload']['Hero'].strip('*')
                    final += 'Team {}{} {}'.format(team, type, hero) + '\n'
                    counter += 1
                    progress += 1
            except(TypeError, KeyError):
                raise
        await bot.say(final + '```')
    except Exception as e:
        raise
#Unfinished
'''
@bot.command(pass_context = True)
async def play(ctx, *, search : str = 'https://www.youtube.com/watch?v=AVy7YPNP_zI'):
    try:
        userid = ctx.message.author.voice_channel.id
    except Exception as e:
        await bot.say('You must join a Voice Channel!')
        return

    try:
        youtubeLink = get_youtube_vid_link(search)
        await bot.say(youtubeLink)
    except(KeyError):
        data = search_videos(search)
        playlistID = data['items'][0]['id']['playlistId']
        youtubeLink = 'https://www.youtube.com/playlist?list={}'.format(playlistID)
        await bot.say(youtubeLink)
    except Exception as e:
        await bot.say('Couldn\'t find a video with that search.')
        return
    channel = bot.get_channel(userid)
    voiceclient = await bot.join_voice_channel(channel)
    discord.opus.is_loaded()
    await bot.say('Getting Music...')
    beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    player = await voiceclient.create_ytdl_player(url = youtubeLink,
                                                  ytdl_options = ytdl_format_options,
                                                  before_options = beforeArgs)

    await bot.say('Song Acquired! Initiating Playback')
    player.start()

@bot.command(pass_context = True)
async def stop(ctx):
    server = ctx.message.server
    voiceclient = bot.voice_client_in(server)
    await voiceclient.disconnect()

@bot.command(pass_context = True)
async def volume(ctx, level : int = 100.0):
    server = ctx.message.server
    try:
        voiceclient = bot.voice_client_in(server)
    except discord.ext.commands.errors.CommandInvokeError:
        await bot.say("You aren't in a voice channel")
        return

    voiceclient.volume = level/100
    await bot.say('Set volume to {}%'.format(level))
'''

#Unusable because of inconsistent file naming
'''
@bot.command(aliases = ['Smbc', 'sbmc','msbc','smcb'])
async def smbc():
    url = 'http://www.smbc-comics.com/random.php'
    response = requests.get(url)
    print(response.url)
    date = response.url[33:]
    date = date.replace('-', '')

    await bot.say('http://www.smbc-comics.com/comics/{}.gif'.format(date))
'''


@bot.event
async def on_ready():
    print(("Logged in as \n{}\n{}\n-------").format(bot.user.name, bot.user.id))
    await bot.change_presence(game=discord.Game(name='Beating up Apparatus'))

@bot.event
async def on_member_join(member):
    channel = chatChannels[member.server]
    message = 'Welcome {} to {}! If You Want to Apply Please Type in +recruit in <#321715129789972483>.'.format(member.mention, member.server)
    await bot.send_message(channel, message)

if __name__ == "__main__":
    bot.run('Removed for Obvious Reasons')

#NayhdBot Token - Removed for Obvious Reasons
#Aetherius Token - Removed for Obvious Reasons
