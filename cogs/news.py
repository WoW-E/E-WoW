from discord.ext import commands
from scraper import NewsScrape, Import, Exterminate, LocaleGet
from db import CreateDatabase, DuplicateCheckUSER, ExportParameter, UpdateParameter, GetUserLocation
from asyncio import sleep


class News(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def news(self, ctx, thing, count=3):
        CreateDatabase('database/location.db')
        locale = GetUserLocation('database/location.db', ctx.message.author.id)
        location = LocaleGet(locale=locale)

        NewsScrape(thing=[f'{thing}'], count=[f'{count}'], location=location)
        titles, links = Import(things=[f'{thing}'])
        Exterminate(things=[f'{thing}'])

        for i, j in zip(titles, links):
            await sleep(0.5)
            await ctx.send(f"{i} - {j}")

    @news.error
    async def news_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("You haven't set a location yet. Please use the 'setlocation' command to set your location.")

    @commands.command()
    async def setlocation(self, ctx, locale):

        countries = ['USA', 'India', 'England', 'Malaysia', 'Vietnam', 'Russia', 'Canada', 'France', 'Germany']

        countries = [x.lower() for x in countries]

        if locale.lower() in countries:

            await ctx.send(f"Hello from {locale}")

            CreateDatabase('database/location.db')
            if DuplicateCheckUSER(ctx.message.author.id):
                ExportParameter(ctx.message.author.id, locale.lower())
                await ctx.send(f'Nice! {ctx.message.author.name} updated his/her location to {locale}.')

            else:
                await ctx.send(f'{ctx.message.author.name} is already in the database with a location, '
                               f'do you want to update your location?')

                def check(m):
                    return m.content.lower() == 'yes' and m.channel == ctx.channel and ctx.message.author.id == m.author.id

                msg = await self.client.wait_for("message", check=check)
                if msg.content.lower() == 'yes':
                    CreateDatabase('database/location.db')
                    UpdateParameter(ctx.message.author.id, locale.lower())
                    await ctx.send(f'Nice! {msg.author} updated his/her location to {locale.lower()}.')
                #
                # def check(m):
                #     return m.content.lower() in countries and m.channel == ctx.channel
                #
                # msg = await self.client.wait_for("message", check=check)
                # if msg.content.lower() in countries:
                #     CreateDatabase('database/location.db')
                #     UpdateParameter(ctx.message.author.id, msg.content.lower())
                #     await ctx.send(f'Nice! {msg.author} updated his/her location to {msg.content.lower()}.')

        else:
            await ctx.send(f"Sorry, News functionality hasn't been expanded to your country yet. Try again later.")


    @setlocation.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send("Trying to inject your code huh? You mf.")


def setup(client):
    client.add_cog(News(client))
