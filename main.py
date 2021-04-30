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
from itertools import cycle
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
        if extension == "all":
            for cog_files in os.listdir('./cogs'):
                if cog_files.endswith('.py'):
                    client.load_extension(f'cogs.{cog_files[:-3]}')
        else:

            client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Successfully loaded {extension}")
    else:
        await ctx.send("Only developers can use this command")


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id in developers:
        if extension == "all":
            for cog_files in os.listdir('./cogs'):
                if cog_files.endswith('.py'):
                    client.unload_extension(f'cogs.{cog_files[:-3]}')
        else:
            client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"Successfully unloaded {extension}")
    else:
        await ctx.send("Only developers can use this command")


@client.command()
async def reload(ctx, extension):
    if ctx.message.author.id in developers:
        if extension == "all":
            for cog_files in os.listdir('./cogs'):
                if cog_files.endswith('.py'):
                    client.unload_extension(f'cogs.{cog_files[:-3]}')
                    client.load_extension(f'cogs.{cog_files[:-3]}')
        else:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
        await ctx.send(f"successfully reloaded {extension}")
    else:
        await ctx.send("Only developers can use this command")


for files in os.listdir('./cogs'):
    if files.endswith('.py'):
        client.load_extension(f'cogs.{files[:-3]}')


@client.command(pass_context=True)
async def help(ctx, command1="help", *command):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)
    command_all = []
    for items in command:
        command_all.append(items)
    prefix = prefixes[str(ctx.guild.id)]
    author = ctx.message.author
    help_embed = discord.Embed(title='Help',
                               description=f"These are all the commands of the bot\nMore information about a command "
                                           f"can be found out using `{prefix}help [command]`",
                               colour=discord.Colour.blue())

    if command1 == "help":
        help_embed.add_field(name='Prefix', value=f"Default Prefix is 'c!'. This server's prefix is `{prefix}`",
                             inline=False)

        help_embed.add_field(name=' :performing_arts: General', value='`bruh` `bye` `hi` `shoot` `thanks`',
                             inline=False)

        help_embed.add_field(name=' :newspaper: News', value='`location` `news` `setlocation`', inline=False)

        help_embed.add_field(name=' :wrench: Utility', value='`ban` `clear` `kick` `ping` `setprefix` `unban`',
                             inline=False)

        help_embed.add_field(name=' :moneybag: Currency', value='`balance`', inline=False)

        if ctx.message.author.id in developers:
            help_embed.add_field(name=' :detective: Developers',
                                 value="`addprefixmanually` `load` `reload` `showprefixes` `unload` ", inline=False)

    else:
        command_all.append(command1)
        for command_items in command_all:
            if command_items == "ban":
                help_embed.add_field(name='ban [user]', value='Bans [user] from the server.', inline=False)
            elif command_items == "bruh":
                help_embed.add_field(name='bruh', value='Shows bruh moment image.', inline=False)
            elif command_items == "bye":
                help_embed.add_field(name='bye', value='Says bye to you.', inline=False)
            elif command_items == "clear":
                help_embed.add_field(name="clear [number of messages]",
                                     value='Deletes [number of messages] which are the most recently sent.')
            elif command_items == "dm":
                help_embed.add_field(name="dm [user] [message]", value='Sends a [message] to [user].')
            elif command_items in ["hi", "hello", "hey"]:
                help_embed.add_field(name=f'hi/hello/hey', value='Greets you hi.', inline=False)
            elif command_items == "kick":
                help_embed.add_field(name='kick [user]', value='Kicks [user] from the server.', inline=False)
            elif command_items == "location":
                help_embed.add_field(name='location',
                                     value='Shows your currently set location')
            elif command_items == "news":
                help_embed.add_field(name='News [News subject] [number of articles]',
                                     value='Gives you [number of articles] on [News subject].')
            elif command_items == "ping":
                help_embed.add_field(name='ping', value='Shows your ping', inline=False)
            elif command_items == "setlocation":
                help_embed.add_field(name='setlocation [location]',
                                     value='Sets your location to [location]. Can be used to change current location '
                                           'too.')
            elif command_items == "setprefix":
                help_embed.add_field(name='setprefix', value='Changes prefix for the server.', inline=False)
            elif command_items == "shoot":
                help_embed.add_field(name='shoot [user]', value='shoots [user] random number of bullets.', inline=False)
            elif command_items == "thanks":
                help_embed.add_field(name='thanks [user]', value='Thanks [user] by mentioning him.', inline=False)
            elif command_items == "unban":
                help_embed.add_field(name='unban [user]', value='Unbans [user] from the server.', inline=False)
            else:
                await ctx.send(f'{command_items} is not a valid command.')
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
