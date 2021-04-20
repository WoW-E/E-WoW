# To Do:
# - Balance
# - Need to make help better - ✓
# - Clear command - ✓
# - Perms error for kick,
# - Perms error for unban - ✓
# - Perms error for ban

import json
import os
import random
import time
from itertools import cycle

import discord
from discord.ext import commands, tasks

from scraper import News, Import, Exterminate, LocaleGet
from db import CreateDatabase, DuplicateCheckUSER, ExportParameter, UpdateParameter, GetUserLocation

if os.path.isdir('database'):
    pass
else:
    os.mkdir('database')


def get_prefix(client, message):
    with open("json_files/prefixes.json", "r") as fprefix:
        prefixes = json.load(fprefix)

        return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')
status = cycle(
    ['Finding Hoomans', 'Killing Hoomans'])


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


@client.event
async def on_ready():
    change_status.start()
    print(f'{client.user.name} has connected to Discord!')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"Successfully kicked {member.mention}")
    await ctx.user.send(f"You were kicked from {member.guild} by {ctx.author} for {reason}")
    await ctx.author.send(f"You kicked {member.display_name} from {member.guild} for {reason}")


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Successfully banned {member.mention}")
    await ctx.user.send(f"You were banned from {member.guild} by {ctx.author} for {reason}")
    await ctx.author.send(f"You banned {member.display_name} from {member.guild} for {reason}")


@client.command()
async def unban(ctx, *, user=None):
    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Error: user could not be found!")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: " + str(ctx.author))
        else:
            await ctx.send("User not banned!")
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("Unbanning failed!")
        return

    await ctx.send(f"Successfully unbanned {user.mention}!")


# @client.command()
# async def start(ctx):
#     with open("balance.json", "r") as fbal:
#         balances1 = json.load(fbal)
#
#     balances1[str(ctx.author.id)] = 0
#
#     with open("balance.json", "w") as fbal:
#         json.dump(balances1, fbal, indent=4)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 100, 2)}ms')


@client.command(aliases=["HI", "hello", "Hello", "Hey", "hey"])
async def hi(ctx):
    await ctx.send('Hi!')


@client.command(aliases=[""])
async def bye(ctx):
    await ctx.send('Bye! ~~Anyways no one was interested in talking to you~~')


@client.command()
async def thanks(ctx, *, user: discord.Member = None):
    if user:
        await ctx.send(f'Yeah, Thank You {user.mention}!!')
    else:
        await ctx.send(
            "Since you didn't *mention* someone, I think you might be thanking me and <@605457586292129840> !!"
        )


# @client.command(name="balance", aliases=['bal', 'cash'])
# async def balance(ctx, *, user: discord.Member = None):
#     with open("balance.json", "r") as fbal:
#         balancesheet = json.load(fbal)
#
#     user_balance = balancesheet[str(ctx.user.id)]
#     await ctx.send(f"{user.mention} has {user_balance}")


@client.command(name='shoot')
async def shoot(ctx, *, user: discord.Member = None):
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
        elif user.id in [605457586292129840, 828858506975117332, 828848983978934292, 732077451601248340]:
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
    await ctx.send(file=discord.File('static/pictures/bruh.jpg'))


@client.command()
@commands.has_permissions(manage_guild=True)
async def clear(ctx, clearno=100):
    await ctx.channel.purge(limit=clearno)
    await ctx.send(f"You cleared {clearno}.")
    time.sleep(1)
    await ctx.channel.purge(limit=1)


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

    help_embed.add_field(name='Prefix', value=f'Default Prefix is "c!". But this server prefix is {prefix}',
                         inline=False)

    help_embed.add_field(name=f'{prefix}help', value='Shows this message dumdum\n', inline=False)

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
    author = ctx.message.author
    if author.id in [605457586292129840, 828858506975117332, 732077451601248340, 828848983978934292]:
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


@client.command()
async def news(ctx, thing, count=3):
    CreateDatabase('database/location.db')
    locale = GetUserLocation('database/location.db', ctx.message.author.id)
    location = LocaleGet(locale=locale)

    News(thing=[f'{thing}'], count=[f'{count}'], location=location)
    titles, links = Import(things=[f'{thing}'])
    Exterminate(things=[f'{thing}'])

    for i, j in zip(titles, links):
        time.sleep(0.5)
        await ctx.send(f"{i} - {j}")


@client.command()
async def setlocation(ctx, locale):

    countries = ['USA', 'India', 'England', 'Malaysia', 'Vietnam', 'Russia', 'Canada', 'France', 'Germany']

    countries = [x.lower() for x in countries]

    if locale.lower() in countries:

        await ctx.send(f"Hello from {locale.lower()}")

        CreateDatabase('database/location.db')
        if DuplicateCheckUSER(ctx.message.author.id):
            ExportParameter(ctx.message.author.id, locale)
            await ctx.send(f'Nice! {ctx.message.author.name} updated his/her location to {locale.lower()}.')

        else:
            await ctx.send(f'{ctx.message.author.name} is already in the database with a location, '
                           f'do you want to update your location?')

            def check(m):
                return m.content.lower() == 'yes' and m.channel == ctx.channel

            msg = await client.wait_for("message", check=check)
            await ctx.send(f"Ok {msg.author}!\n\nWhich location do you want to update to?")

            def check(m):
                return m.content.lower() in countries and m.channel == ctx.channel


            msg = await client.wait_for("message", check=check)
            if msg.content.lower() in countries:
                CreateDatabase('database/location.db')
                UpdateParameter(ctx.message.author.id, msg.content.lower())
                await ctx.send(f'Nice! {msg.author} updated his/her location to {msg.content.lower()}.')

    else:
        await ctx.send(f"Sorry, News functionality hasn't been expanded to your country yet. Try again later.")


client.run(os.getenv('TOKEN'))
