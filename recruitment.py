import discord
from discord.ext import commands

class Recruitment:

    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def recruit(self, ctx):

        #IGN
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('Hi {}! Glad to see you want to apply to join the guild!'.format(ctx.message.author))
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'IGN',
                           value='What\'s your IGN?')
        await self.bot.say(embed = embedded)
        ign = await self.bot.wait_for_message(author=ctx.message.author)

        #Rank
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color=discord.Color.dark_grey())
        embedded.add_field(name = 'Rank',
                           value = 'What Rank were you in Spring Season 2017?\n(You must be higher than Tier 7 and provide a picture of proof')
        await self.bot.say(embed = embedded)
        rank = await self.bot.wait_for_message(author = ctx.message.author)

        #Experience
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color=discord.Color.dark_grey())
        embedded.add_field(name = 'Experience',
                           value='How long have you been playing VainGlory?')
        await self.bot.say(embed = embedded)
        experience = await self.bot.wait_for_message(author = ctx.message.author)

        #Voice Chat
        await self.bot.send_typing(ctx.message.channel)
        embedded=discord.Embed(color=discord.Color.dark_grey())
        embedded.add_field(name = 'Voice Chat',
                           value = 'How comfortable are you using Voice Chat?\nIf not, this is not the guild for you.')
        await self.bot.say(embed = embedded)
        voice_chat = await self.bot.wait_for_message(author = ctx.message.author)

        #Wins
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Wins',
                           value = 'How many wins do you have?')
        await self.bot.say(embed = embedded)
        wins = await self.bot.wait_for_message(author = ctx.message.author)

        #Discord Activity
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Discord Activity',
                           value = 'Will you be able to be active on Discord?')
        await self.bot.say(embed = embedded)
        discord_activity = await self.bot.wait_for_message(author=ctx.message.author)

        #Role
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Role',
                           value = 'What is your preferred role?')
        await self.bot.say(embed = embedded)
        role = await self.bot.wait_for_message(author=ctx.message.author)

        #Age
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Age',
                           value = 'How old are you?\n(12 years old and higher)')
        await self.bot.say(embed = embedded)
        age = await self.bot.wait_for_message(author=ctx.message.author)

        #Game Activity
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Game Activity',
                           value = 'How would you rate yourself 1-10 on how active you are?')
        await self.bot.say(embed = embedded)
        activity = await self.bot.wait_for_message(author=ctx.message.author)

        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.green())
        embedded.add_field(
            name = 'IGN',
            value = ign
        )
        embedded.add_field(
            name='Rank',
            value= rank
        )
        embedded.add_field(
            name='Experience',
            value = experience
        )
        embedded.add_field(
            name='Voice Chat',
            value= voice_chat
        )
        embedded.add_field(
            name='Wins',
            value= wins
        )
        embedded.add_field(
            name='Activity on Discord',
            value=discord_activity
        )
        embedded.add_field(
            name='Role',
            value=role
        )
        embedded.add_field(
            name='Age',
            value=age
        )
        embedded.add_field(
            name='Game Activity',
            value=activity
        )
        await self.bot.say(embed = embedded)