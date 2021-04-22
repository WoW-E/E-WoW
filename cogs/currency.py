import discord
from discord.ext import commands
import json


class Balance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="balance", aliases=['bal', 'cash'])
    async def balance(ctx, *, user: discord.Member = None):
        with open("balance.json", "r") as fbal:
            balancesheet = json.load(fbal)

        user_balance = balancesheet[str(ctx.user.id)]
        await ctx.send(f"{user.mention} has {user_balance}")


def setup(client):
    client.add_cog(Balance(client))
