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
import time


owm = pyowm.OWM('3efe1d1446293d1db9d885956d91ebf5')
cw = CleverWrap('CC28sjh2gAso-_swa8qaAIREAPw')
bot = commands.Bot(command_prefix='+', description='NayhdBot')
bot.add_cog(Music(bot))
bot.add_cog(Poll(bot))
bot.add_cog(Recruitment(bot))
api_key = 'AIzaSyAiQXR2zB7MKJLKu-Wb2h6GLzyyEK8Veck'
service = build('youtube', 'v3', developerKey=api_key)
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
        'api_key': 'MTkxMDQz',
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
    await bot.send_typing(ctx.message.channel)
    startTime = time.monotonic()
    await (await bot.ws.ping())
    endTime = time.monotonic()
    ping = (endTime - startTime) * 1000
    await bot.say('The server response time was {}ms'.format(int(ping)))


@bot.command(pass_context = True, aliases = ['Clever','cleverbot','Cleverbot'])
async def clever(ctx, *, input: str):
    await bot.send_typing(ctx.message.channel)
    embedded = discord.Embed(title = cw.say(input), color = discord.Color.gold())
    await bot.say(embed = embedded)

@bot.command(pass_context = True)
async def urban(ctx, *, input: str):
    try:
        url = 'https://mashape-community-urban-dictionary.p.mashape.com/define'
        parameters = {
            'term':input
        }
        headers = {
            "X-Mashape-Key": "cUUxNDHnECmsh9142gYgZNRCIVSlp1BBt5GjsnB5ijViJLZJuJ",
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


@bot.command(pass_context = True, aliases = ['Clear','wipe','Wipe'])
async def clear(ctx, number : int = 50):
    try:
        clearlist = open('clearlist.txt', 'r').read().splitlines()
        if ctx.message.author.id in clearlist:
            pass
        else:
            await bot.send_typing(ctx.message.channel)
            await bot.say("You're not authorized")
            return

        deleted = await bot.purge_from(ctx.message.channel, limit = number)
        #await bot.send_message(ctx.message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    except Exception as e:
        print(e)
        deleted = await bot.purge_from(ctx.message.channel, limit=1)
        await bot.send_message(ctx.message.channel, "Can't delete messages older than 14 days.")


@bot.command(pass_context = True, aliases = ['mobcrush','Mob','Mobcrush'])
async def mob(ctx, name: str = 'mobcrush'):
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
    await bot.send_typing(ctx.message.channel)
    await bot.say(get_xkcd_url(get_xkcd_num()))


@bot.command(pass_context = True, aliases = ['logout','logoff'])
async def shutdown(ctx):
    await bot.send_typing(ctx.message.channel)
    admins = open('adminlist.txt','r').read().splitlines()
    if ctx.message.author.id in admins:
        await bot.say("Logging Off")
        await bot.logout()
    else:
        await bot.say("You're not authorized to do this")


@bot.command(pass_context=True, aliases=['eric', 'cats', 'Cat', 'Eric'])
async def cat(ctx, num: int = 1):
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
    adminlist = open('adminlist.txt').read().splitlines()
    if ctx.message.author.id in adminlist:
        for step in range(times):
            await bot.send_typing(ctx.message.channel)
            await bot.say(statement)
    else:
        await bot.send_typing(ctx.message.channel)
        await bot.say('Yeah... No')

@bot.command(pass_context = True)
async def draft(ctx, ign : str = 'dpp2000', region: str = 'na'):
    try:
        dpp_api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJhMWYzZjQzMC0xYjNkLTAxMzUtMGQ5ZC0wMjQyYWMxMTAwMDciLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNDk0ODEyNTI4LCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJhMWYyYmY3MC0xYjNkLTAxMzUtMGQ5Yi0wMjQyYWMxMTAwMDciLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.Fc2IQwIkmVp8RfJ7bsmp_DWgEse7tS6y8BXMBiTIuIY'
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

#Unusable because of inconsistent file naming by SMBC
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
    message = 'Welcome {} to {}!'.format(member.mention, member.server)
    await bot.send_message(channel, message)

if __name__ == "__main__":
    bot.run('MzI5NDU0NDczNTk0NDA0ODY2.DDSr5Q.yp-HzJV1Ig4VB6_2SWE1nJGG044')
