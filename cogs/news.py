from asyncio import sleep
import discord
from discord.ext import commands

from db import DatabaseInit, DuplicateCheckUser, ExportParameter, UpdateParameter, GetUserLocation
from scraper import NewsScrape, Import, Exterminate, LocaleGet


class News(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def news(self, ctx, count, *things):
        DatabaseInit(database='main', table='location', user_id='integer', location='text')
        locale = GetUserLocation(user=ctx.message.author.id)
        location_user = LocaleGet(locale=locale)

        parameter = []
        for value in things:
            param = "{}".format(value)
            parameter.append(param)

        thing = "%20".join(parameter)

        NewsScrape(thing=[f'{thing}'], count=[f'{count}'], location=location_user)
        titles, links = Import(things=[f'{thing}'])
        Exterminate(things=[f'{thing}'])

        for i, j in zip(titles, links):
            await sleep(0.5)
            await ctx.send(f"{i} - {j}")


    @news.error
    async def news_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"You haven't set a location yet {ctx.message.author.mention}. Set a location using the `setlocation` command.")

    @commands.command()
    async def setlocation(self, ctx, locale):

        countries = ['USA', 'India', 'England', 'Malaysia', 'Vietnam', 'Russia', 'Canada', 'France', 'Germany']

        countries = [x.lower() for x in countries]

        if locale.lower() in countries:

            await ctx.send(f"Hello from {locale}")

            DatabaseInit(database='main', table='location', user_id='integer', location='text')
            if DuplicateCheckUser(database='main', table='location', user=ctx.message.author.id):
                if ExportParameter(database='main', table='location', user=ctx.message.author.id,
                                   location=locale.lower()):
                    await ctx.send(f'Nice! {ctx.message.author.name} set their location to {locale}.')
                else:
                    await ctx.send(
                        f"Something went wrong :-( \nReporting problem to the devs. They aren't going to like this!")

            else:
                await ctx.send(f'{ctx.message.author.name} is already in the database with the location: '
                               f'`{GetUserLocation(user=ctx.message.author.id)}`, do you want to update your location?')

                def check(m):
                    return m.content.lower() == 'yes' and m.channel == ctx.channel and ctx.message.author.id == m.author.id

                msg = await self.client.wait_for("message", check=check)
                if msg.content.lower() == 'yes':
                    DatabaseInit(database='main', table='location', user_id='integer', location='text')
                    UpdateParameter(database='main', table='location', user=ctx.message.author.id,
                                    location=locale.lower())
                    await ctx.send(f'Nice! {msg.author} updated his/her location to {locale.lower()}.')

        else:
            await ctx.send(f"Sorry, News functionality hasn't been expanded to `{locale}`yet. Try again later.")

    @setlocation.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send("Trying to inject your code huh? You mf.")

    @commands.command()
    async def location(self, ctx):
        location_embed = discord.Embed(title='Location',
                                       description=f"{ctx.message.author.mention}'s location is `{GetUserLocation(user=ctx.message.author.id)}.`",
                                       colour=discord.Colour.blue())
        await ctx.send(ctx.message.author.mention, embed=location_embed)

    @location.error
    async def location_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"You haven't set a location yet {ctx.message.author.mention}. Set a location using the `setlocation` command.")


def setup(client):
    client.add_cog(News(client))
