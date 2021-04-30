import random

import discord
from discord.ext import commands
from asyncio import sleep

developers = [605457586292129840, 828858506975117332, 828848983978934292, 732077451601248340]


class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 100, 2)}ms')

    @commands.command(aliases=["HI", "hello", "Hello", "Hey", "hey"])
    async def hi(self, ctx):
        await ctx.send('Hi!')

    @commands.command(aliases=["Goodbye"])
    async def bye(self, ctx):
        msg = await ctx.send('Bye!')
        await sleep(3)
        await msg.edit(content="Bye! ~~Anyways no one was interested in talking to you~~")

    @commands.command()
    async def thanks(self, ctx, *, user: discord.Member = None):
        if user:
            await ctx.send(f'Yeah, Thank You {user.mention}!!')
        else:
            await ctx.send(
                "Since you didn't *mention* someone, I think you might be thanking me and the awesome developers who "
                "made me !! "
            )

    @commands.command()
    async def shoot(self, ctx, *, user: discord.Member = None):
        if user:
            await ctx.send(f"You are trying to shoot {user.mention}")
            if user.bot:
                await ctx.send('You trying to shoot the bots but...')
                await ctx.send(file=discord.File('static/gifs/uno-reverse.gif'))
                await ctx.send(
                    f'{ctx.message.author.mention} DIED. NO F/RIP for you! Trying to kill a bot huh!'
                )
            elif user.id == ctx.message.author.id:
                await ctx.send(
                    f'{ctx.message.author.mention} Killing yourself is bad!!'
                )
            elif user.id in developers:
                await ctx.send(
                    'How dare you try to shoot the super fantastic awesome guy who made me!! Go shoot someone else!!'
                )
            else:
                random_num = random.randint(1, 1000)
                await ctx.send(
                    f'{user.mention} was shot {random_num} times in the head! OOF')
        else:
            await ctx.send(
                'You only had one bullet. Next time *mention* who to shoot')

    @commands.command()
    async def bruh(self, ctx):
        await ctx.send(file=discord.File('static/pictures/bruh.jpg'))


def setup(client):
    client.add_cog(General(client))
