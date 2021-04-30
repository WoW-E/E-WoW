import discord
from discord.ext import commands
import inspect

developers = [605457586292129840, 828858506975117332, 828848983978934292, 732077451601248340]


class Execute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=["exec"])
    async def execute(self, ctx, *, code: str):
        if ctx.message.author.id in developers:
            code = code.strip('` ')
            python = '```py\n{}\n```'
            result = None

            env = {
                'client': self.client,
                'ctx': ctx,
                'message': ctx.message,
                'server': ctx.message.guild,
                'channel': ctx.message.channel,
                'author': ctx.message.author
            }

            env.update(globals())

            try:
                result = eval(code, env)
                if inspect.isawaitable(result):
                    result = await result
            except Exception as e:
                await ctx.send(python.format(type(e).__name__ + ': ' + str(e)))
                return
        else:
            ctx.send("Only developers can use this command")


def setup(client):
    client.add_cog(Execute(client))
