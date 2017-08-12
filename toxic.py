import discord
from discord.ext import commands
import asyncio, json

class Toxic:
    toxic_players = open('DataFiles/toxic.json', )
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def toxic(self, ctx, toxic_players, *, players : str = None):
        try:
            if ctx.message.author.id in toxic_players:
                pass
            else:
                print(toxic_players[ctx.message.author.id])
                toxic_players[ctx.message.author.id] = []

            for player in players.split(' '):
                print(toxic_players[ctx.message.author.id])
                toxic_players[ctx.message.author.id].append(player)
            #toxic_players.sync()
        except Exception as e:
            await self.bot.say(e)

    @commands.command(pass_context = True)
    async def tox(self, ctx, toxic_players, player : str = None):
        if player in toxic_players[ctx.message.author.id]:
            embedded = discord.Embed(color = discord.Color.red())
            embedded.set_author(name='Toxic!')
            await self.bot.say(embed = embedded)
        else:
            embedded = discord.Embed(color = discord.Color.green())
            embedded.set_author(name = 'Safe!')
            await self.ot.say(embed = embedded)

    @commands.command(pass_context = True)
    async def toxlist(self, ctx, toxic_players):
        message = '```\nToxic List\n'
        try:
            for player in toxic_players[ctx.message.author.id]:
                message += '\n{}'.format(player)
        except Exception as e:
            print(e)
            return
        message+='\n```'
        await self.bot.say(message)

    @commands.command(pass_context = True)
    async def clean(self, ctx, toxic_players, player : str = 'Aethen'):
        try:
            toxic_players[ctx.message.author.id].remove(player)
            await self.bot.say('Success')
        except Exception as e:
            await self.bot.say(e)