import discord
from discord.ext import commands
from pprint import pprint

class Poll:
    def __init__(self, bot):
        self.bot = bot
        self.polls = {}
        self.pollKeys = []
        self.answerKeys = []

    @commands.command(pass_context = True, aliases = ['startpoll'])
    async def startPoll(self, ctx, *, question : str = None):
        #Makes sure Question was Asked
        if question == None:
            await self.bot.say('Please include a Question')
            return
        try:
            self.polls[ctx.message.author.id] = {}
            self.polls[ctx.message.author.id]['question'] = question
            self.polls[ctx.message.author.id]['user'] = ctx.message.author
            self.polls[ctx.message.author.id]['votes'] = []
            self.polls[ctx.message.author.id]['score'] = 0
            self.polls[ctx.message.author.id]['answers'] = {}
            #if self.polls[ctx.message.author.id] == None:
            embedded = discord.Embed(color = discord.Color.gold())
            embedded.description = 'How many Answer Choices are there?'
            await self.bot.say(embed = embedded)
            choices = await self.bot.wait_for_message(author = ctx.message.author)
            if int(choices.content) > 5:
                await self.bot.say('Sorry, I can only handle up to 5 Answers')
                return
            try:
                choices = abs(int(choices.content))
                answers = []
            except ValueError:
                await self.bot.say('That\'s not a Integer')
                return
            for step in range(choices):
                embedded.description = 'What\'s answer Number {}?'.format(step + 1)
                await self.bot.say(embed = embedded)
                answer = await self.bot.wait_for_message(author = ctx.message.author)
                answers.append(answer.content)

            for solution in answers:
                self.polls[ctx.message.author.id]['answers'][solution] = 0
            pprint(self.polls)

            output = ''
            step = 1
            for key in self.polls[ctx.message.author.id]['answers']:
                output += '{}. {}\n'.format(step, key)
                step += 1

            #for answer in range(len(self.polls[ctx.message.author.id]['answers'])):
            #    output += '{}. {}\n'.format(answer+1 ,self.polls[ctx.message.author.id]['answers'][answer])


            embedded.color = discord.Color.green()
            embedded.title = 'New Poll Successfully Created!'
            embedded.description = ''
            embedded.add_field(
                name = question,
                value = output,
                inline = True
            )
            await self.bot.say(embed = embedded)
        except(KeyError):
            embedded = discord.Embed(
                color = discord.Color.red(),
                title = 'WARNING',
                description = 'It appears you already have a registered Poll. Would you like to overwrite it?'
            )
            await self.bot.say(embed = embedded)
            resetBool = await self.bot.wait_for_message(author = ctx.message.author)
            if resetBool.lower() == 'yes':
                del self.polls[ctx.ctx.message.author.id]
                await ctx.invoke(self.startPoll, question=question)


    @commands.command(pass_context = True)
    async def vote(self, ctx):
        embedded = discord.Embed(
            title = 'Which Poll would you like to Vote in?',
            color = discord.Color.gold()
        )
        step = 1
        for key in self.polls:
            self.pollKeys.append(key)
            embedded.add_field(
                name = '{}. {}'.format(step, self.polls[key]['user']),
                value = self.polls[key]['question'],
                inline = False
            )
            step += 1
        msg = await self.bot.say(embed = embedded)
        reactions = ['\U00000031\U000020e3','\U00000032\U000020e3','\U00000033\U000020e3','\U00000034\U000020e3','\U00000035\U000020e3']

        for reaction in range(len(reactions)):
            if reaction+1 <= len(self.polls):
                await self.bot.add_reaction(msg,reactions[reaction])
            else:
                break
        reaction = await self.bot.wait_for_reaction(user = ctx.message.author, message = msg)
        #print(reaction.reaction.emoji == reactions[0])
        for check in reactions:
            if reaction.reaction.emoji == check:
                #print(reactions.index(reaction.reaction.emoji))
                pollselection = self.polls[self.pollKeys[reactions.index(reaction.reaction.emoji)]]

                break
        pprint(pollselection)
        output = ''
        step = 1
        for answer in pollselection['answers']:
            output += '{}. {}\n'.format(step, answer)
            step += 1

        embedded = discord.Embed(
            color = discord.Color.gold(),
            title = 'Which Answer would you like to pick?'
        )
        embedded.add_field(
            name = pollselection['question'],
            value = output,
            inline = False
        )
        msg =await self.bot.say(embed = embedded)
        for answer in range(len(pollselection['answers'])):
            await self.bot.add_reaction(msg, reactions[answer])
        step = 0
        for answer in pollselection['answers']:
            self.answerKeys.append(answer)
            await self.bot.add_reaction(msg, reactions[step])
            step += 1
        reaction = await self.bot.wait_for_reaction(user=ctx.message.author, message=msg)
        reaction = reactions.index(reaction.reaction.emoji)
        authorId = pollselection['user'].id
        self.polls[authorId]['answers'][self.answerKeys[reaction]] += 1
        self.polls[authorId]['votes'].append(ctx.message.author.id)
        self.answerKeys = []
        #pollselection['answers'][self.answerKeys[reaction]] += 1
        pprint(self.polls)