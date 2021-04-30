import json

import discord
from discord.ext import commands


class Balance(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="balance", aliases=['bal', 'cash', 'money'])
    async def balance(self, ctx, *, user: discord.User = None):
        with open("json_files/balance.json", "r") as fbal:
            balancesheet = json.load(fbal)
        try:
            if user:
                user_balance = balancesheet[str(user.id)]
                await ctx.send(f"{user.mention} has {str(user_balance)}")

            else:
                user_balance = balancesheet[str(ctx.message.author.id)]
                await ctx.send(f"{ctx.message.author.mention} has {str(user_balance)}")
        except KeyError:
            if user:
                balancesheet[str(user.id)] = 0

                with open("json_files/balance.json", "w") as fbal:
                    json.dump(balancesheet, fbal, indent=4)

                await ctx.send(f"{user.mention} has 0")

            else:
                balancesheet[str(ctx.message.author.id)] = 0

                with open("json_files/balance.json", "w") as fbal:
                    json.dump(balancesheet, fbal, indent=4)

                await ctx.send(f"{ctx.message.author.id} has 0")


def setup(client):
    client.add_cog(Balance(client))
