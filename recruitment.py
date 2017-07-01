import discord
from discord.ext import commands
from discord.errors import HTTPException

class Recruitment:

    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def recruit(self, ctx):

        #IGN
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.say('Hi {}! Glad to see you want to apply to join the guild!'.format(ctx.message.author.mention))
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'IGN',
                           value='What\'s your IGN?')
        one = await self.bot.say(embed = embedded)
        ign = await self.bot.wait_for_message(author=ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(ign)

        #Rank
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color=discord.Color.dark_grey())
        embedded.add_field(name = 'Rank',
                           value = 'What Rank were you in Spring Season 2017?\n(You must be higher than Tier 7)')
        one = await self.bot.say(embed = embedded)
        rank = await self.bot.wait_for_message(author = ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(rank)

        #Rank Picture
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Rank Picture',
                           value = 'Please send a picture of your Ranked Trophy from Spring Season 2017.')
        one = await self.bot.say(embed = embedded)
        rank_pic = await self.bot.wait_for_message(author = ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(rank_pic)

        #Experience
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color=discord.Color.dark_grey())
        embedded.add_field(name = 'Experience',
                           value='How long have you been playing VainGlory?')
        one = await self.bot.say(embed = embedded)
        experience = await self.bot.wait_for_message(author = ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(experience)

        #Voice Chat
        await self.bot.send_typing(ctx.message.channel)
        embedded=discord.Embed(color=discord.Color.dark_grey())
        embedded.add_field(name = 'Voice Chat',
                           value = 'How comfortable are you using Voice Chat?\nIf not, this is not the guild for you.')
        one = await self.bot.say(embed = embedded)
        voice_chat = await self.bot.wait_for_message(author = ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(voice_chat)

        #Wins
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Wins',
                           value = 'How many wins do you have?')
        one = await self.bot.say(embed = embedded)
        wins = await self.bot.wait_for_message(author = ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(wins)

        #Discord Activity
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Discord Activity',
                           value = 'Will you be able to be active on Discord?')
        one = await self.bot.say(embed = embedded)
        discord_activity = await self.bot.wait_for_message(author=ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(discord_activity)

        #Role
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Role',
                           value = 'What is your preferred role?')
        one = await self.bot.say(embed = embedded)
        role = await self.bot.wait_for_message(author=ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(role)

        #Age
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Age',
                           value = 'How old are you?\n(12 years old and higher)')
        one = await self.bot.say(embed = embedded)
        age = await self.bot.wait_for_message(author=ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(age)


        #Game Activity
        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.dark_grey())
        embedded.add_field(name = 'Game Activity',
                           value = 'How would you rate yourself 1-10 on how active you are?')
        one = await self.bot.say(embed = embedded)
        activity = await self.bot.wait_for_message(author=ctx.message.author)
        await self.bot.delete_message(one)
        await self.bot.delete_message(activity)

        await self.bot.send_typing(ctx.message.channel)
        embedded = discord.Embed(color = discord.Color.green())
        embedded.add_field(
            name = 'IGN',
            value = ign.content
        )
        embedded.add_field(
            name='Rank',
            value= rank.content
        )
        embedded.add_field(
            name='Experience',
            value = experience.content
        )
        embedded.add_field(
            name='Voice Chat',
            value= voice_chat.content
        )
        embedded.add_field(
            name='Wins',
            value= wins.content
        )
        embedded.add_field(
            name='Activity on Discord',
            value=discord_activity.content
        )
        embedded.add_field(
            name='Role',
            value=role.content
        )
        embedded.add_field(
            name='Age',
            value=age.content
        )
        embedded.add_field(
            name='Game Activity',
            value=activity.content
        )
        embedded.set_image(url = rank_pic.attachments[0]['url'])
        #embedded.set_footer(text = 'Thank you for applying! Please post a picture of your highest Skill Tier.')
        try:
            await self.bot.say(embed = embedded)
        except HTTPException:
            await self.bot.say('Please try again, and keep all responses in text file. No pictures.')