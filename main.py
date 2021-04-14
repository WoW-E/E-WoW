import os
import random
import json
import discord
from discord.ext import commands

from keep_alive import keep_alive

client = commands.Bot(command_prefix='c!')
client.remove_command('help')


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 100, 2)}ms')


@client.command()
async def hi(ctx):
    await ctx.send('Hi!')


@client.command()
async def hello(ctx):
    await ctx.send('Hi man!! Good to see you')


@client.command()
async def bye(ctx):
    await ctx.send('Bye! ~Anyways no one was interested in talking to you~')


@client.command()
async def thanks(ctx, *, user: discord.Member = None):
    if user:
        await ctx.send(f'Yeah, Thank You {user.mention}!!')
    else:
        await ctx.send(
            "Since you didn't *mention* someone, I think you might be thanking me and <@605457586292129840> !!"
        )


##def get_prefix(client,message):
##    with open(prefixes.json, "r") as fprefix:
##        prefixes = json.load()
##        return prefixes[]


@client.command(name='shoot')
async def shoot(ctx, *, user: discord.Member = None):
    if user:
        await ctx.send(f"You are trying to shoot {user.mention}")
        if user.bot:
            await ctx.send('You trying to shoot the bots but...')
            await ctx.send(file=discord.File('uno-reverse.gif'))
            await ctx.send(
                f'{ctx.message.author.mention} DIED. NO F/RIP for you! Trying to kill a bot huh!'
            )
        elif user.id == ctx.message.author.id:
            await ctx.send(
                f'{ctx.message.author.mention} Killing yourself is bad!!'
            )
        elif user.id == 605457586292129840 or 828858506975117332 or 828848983978934292 or 732077451601248340:
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


@client.command()
async def bruh(ctx):
    await ctx.send(file=discord.File('bruh.jpg'))


@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    random_opt = random.randint(0, 2)
    if random_opt == 1:
        help_embed = discord.Embed(colour=discord.Colour.orange())
    elif random_opt == 2:
        help_embed = discord.Embed(colour=discord.Colour.red())
    else:
        help_embed = discord.Embed(colour=discord.Colour.green())
    help_embed.set_author(name='Help')
    help_embed.add_field(name='Prefix', value='Prefix is "c!"', inline=False)
    help_embed.add_field(name='c!help',
                         value='Shows this message dumdum',
                         inline=False)
    help_embed.add_field(name='c!ping', value='Shows your ping', inline=False)
    help_embed.add_field(name='c!hi/hello', value='Greets you', inline=False)
    help_embed.add_field(
        name='c!bye',
        value='says bye to you (:warning: Warning, its toxic!).',
        inline=False)
    help_embed.add_field(name='c!thanks {user}',
                         value='Thanks the person you mention',
                         inline=False)
    help_embed.add_field(name='c!shoot {user}',
                         value='shoots someone',
                         inline=False)
    help_embed.add_field(name='c!bruh',
                         value='shows a image showing bruh moment',
                         inline=False)

    await ctx.send(author.mention, embed=help_embed)


@client.command()
async def dm(ctx, user: discord.Member = None, *, message=None):
    author = ctx.message.author
    if author.id == 605457586292129840:
        if user:
            if message is None:
                await ctx.send('No message')
            else:
                await user.send(message)
                await ctx.channel.purge(limit=1)
                await ctx.author.send('"' + message + '"' + ' sent to ' +
                                      str(user))
                print('"' + message + '"' + ' sent to ' + str(user))
        else:
            await ctx.send('No User')
    else:
        await ctx.send('Invalid Command?')


keep_alive()

client.run('ODI4ODUxNjUwMzc4MjAzMTQ2.YGvmQA.EPYXl3jwbGxmkAMP46Aw_8WwrJI')
