# To Do:
# - Balance
# - Optimize help command -
# - Snakes and Ladders -
# - Need to make help better - ✓
# - Clear command - ✓
# - Perms error for kick - ✓
# - Perms error for unban - ✓
# - Perms error for ban - ✓

import json
import os
import random
from itertools import cycle
from asyncio import sleep
import discord
from discord.ext import commands, tasks

if os.path.isdir('database'):
    pass
else:
    os.mkdir('database')

developers = [605457586292129840, 828858506975117332, 828848983978934292, 732077451601248340]


def get_prefix(client, message):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)

        return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')
status = cycle(
    ['Finding Hoomans [1/2]', 'Killing Hoomans [2/2]'])


@client.event
async def on_guild_join(guild):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)

    prefixes[str(guild.id)] = 'c!'

    with open("json_files/prefixes.json", "w") as fprefix:
        json.dump(prefixes, fprefix, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)

    prefixes.pop(str(guild.id))

    with open("json_files/prefixes.json", "w") as fprefix:
        json.dump(prefixes, fprefix, indent=4)


@client.command()
@commands.has_permissions(manage_guild=True)
async def setprefix(ctx, prefix):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)

    prefixes[str(ctx.guild.id)] = prefix
    await ctx.send(f'Prefix successfully changed to {prefix}')

    with open("json_files/prefixes.json", "w") as fprefix:
        json.dump(prefixes, fprefix, indent=4)


@client.command()
async def addprefixmanually(ctx, guildid, guildprefix):
    if ctx.message.author.id in developers:
        with open("json_files/prefixes.json", "r") as fprefix:
            prefixes = json.load(fprefix)

        prefixes[guildid] = guildprefix
        await ctx.send(f'Prefix of {guildid} successfully changed to {guildprefix}')

        with open("json_files/prefixes.json", "w") as fprefix:
            json.dump(prefixes, fprefix, indent=4)
    else:
        await ctx.send("No perms")


@client.command()
async def showprefixes(ctx):
    if ctx.message.author.id in developers:
        with open("json_files/prefixes.json", "r") as fprefix:
            prefixes = json.load(fprefix)

        await ctx.send(str(json.dumps(prefixes, indent=4)))
    else:
        await ctx.send("Sorry, this command can be only used by this bot devs.")


@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user.name} has connected to Discord!')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def load(ctx, extension):
    if ctx.message.author.id in developers:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"successfully loaded {extension}")
    else:
        await ctx.send("Only developers can use this command")


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id in developers:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"successfully unloaded {extension}")
    else:
        await ctx.send("Only developers can use this command")


@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id in developers:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"successfully reloaded {extension}")
    else:
        await ctx.send("Only developers can use this command")


for files in os.listdir('./cogs'):
    if files.endswith('.py'):
        client.load_extension(f'cogs.{files[:-3]}')


@client.command(pass_context=True)
async def help(ctx):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)

    prefix = prefixes[str(ctx.guild.id)]
    author = ctx.message.author
    random_opt = random.randint(0, 2)
    if random_opt == 1:
        help_embed = discord.Embed(colour=discord.Colour.orange())
    elif random_opt == 2:
        help_embed = discord.Embed(colour=discord.Colour.red())
    else:
        help_embed = discord.Embed(colour=discord.Colour.green())
    help_embed.set_author(name='Help')

    help_embed.add_field(name='Prefix', value=f"Default Prefix is 'c!'. This server's prefix is {prefix}.",
                         inline=False)

    help_embed.add_field(name=f'{prefix}help', value='Shows this message dumdum', inline=False)

    help_embed.add_field(name=f'{prefix}setprefix', value='Changes prefix for the server', inline=False)

    help_embed.add_field(name=f'{prefix}hi/hello/hey', value='Greets you hi', inline=False)

    help_embed.add_field(name=f'{prefix}ping', value='Shows your ping', inline=False)

    help_embed.add_field(name=f'{prefix}shoot [user]', value='shoots someone', inline=False)

    help_embed.add_field(name=f'{prefix}bruh', value='shows a image showing bruh moment', inline=False)

    help_embed.add_field(name=f"{prefix}clear [number of messages]",
                         value='Deletes [number of messages] which are the most recently sent.')

    # help_embed.add_field(name=f"{prefix}dm [user] [message]", value='Sends a [message] to [user].')

    help_embed.add_field(name=f'{prefix}kick [user]', value='Kicks [user] from the server.', inline=False)

    help_embed.add_field(name=f'{prefix}ban [user]', value='Bans [user] from the server.', inline=False)

    help_embed.add_field(name=f'{prefix}unban [user]', value='Unbans [user] from the server.', inline=False)

    help_embed.add_field(name=f'{prefix}news [news subject] [number of articles]',
                         value='Gives you [number of articles] on [news subject].')

    help_embed.add_field(name=f'{prefix}bye', value='Says bye to you.', inline=False)

    help_embed.add_field(name=f'{prefix}thanks [user]', value='Thanks the person you mention', inline=False)
    await ctx.send(author.mention, embed=help_embed)


@client.command()
async def dm(ctx, user: discord.Member = None, *, message=None):
    if ctx.message.author.id in developers:
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


client.run(os.getenv('TOKEN'))
