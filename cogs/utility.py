import discord
from discord.ext import commands
from asyncio import sleep


class utility(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        msg = await ctx.send("Checking Perms...")
        await sleep(0.5)
        if isinstance(ctx.channel, discord.channel.DMChannel):
            msg.edit(content="Can you teach me how to kick someone in dms?")

        else:
            if ctx.message.guild.me.guild_permissions.kick_members:
                if ctx.message.author.guild_permissions.kick_members:
                    await msg.edit(content="Permissions are valid, checking user you are trying to kick")
                    if member.id == ctx.message.guild.owner_id:
                        await msg.edit(content="You can't kick the owner of the server!")
                    else:
                        if member == ctx.message.guild.me:
                            await msg.edit(content=f"{ctx.message.author.mention}You can't defeat me by using me")
                        else:
                            await msg.edit(content=f"Trying to kick {member.mention}")
                            await sleep(2)
                            await member.send(
                                f"You are being kicked from {member.guild.name} by {ctx.message.author}\n Reason is {reason}")
                            await member.kick(reason=reason)
                            await msg.edit(content=f"Successfully kicked {member}")
                else:
                    msg.edit(content="You are missing permissions")
            else:
                msg.edit(content="I am missing permission")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Error!! The person you are trying to kick might be on the same or higher role")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        msg = await ctx.send("Checking Perms...")
        await sleep(0.5)
        if isinstance(ctx.channel, discord.channel.DMChannel):
            msg.edit(content="Can you teach me how to ban someone in dms?")

        else:
            if ctx.message.guild.me.guild_permissions.ban_members:
                if ctx.message.author.guild_permissions.ban_members:
                    await msg.edit(content="Permissions are valid, checking user you are trying to kick")
                    if member.id == ctx.message.guild.owner_id:
                        await msg.edit(content="You can't ban the owner of the server!")
                    else:
                        if member == ctx.message.guild.me:
                            await msg.edit(content=f"{ctx.message.author.mention}You can't defeat me by using me")
                        else:
                            await msg.edit(content=f"Trying to ban {member.mention}")
                            await sleep(2)
                            await member.ban(reason=reason)
                            await member.send(
                                f"You are being banned from {member.guild.name} by {ctx.message.author}\n Reason is {reason}")
                            await msg.edit(content=f"Successfully banned {member.mention}")
                else:
                    msg.edit(content="You are missing permissions")
            else:
                msg.edit(content="I am missing permission")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Error!! The person you are trying to ban might be on the same or higher role")

    @commands.command()
    async def unban(self, ctx, *, user=None):
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

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def clear(self, ctx, clearno=100):
        await ctx.channel.purge(limit=clearno)
        await ctx.send(f"You cleared {clearno}.")
        await sleep(1)
        await ctx.channel.purge(limit=1)


def setup(client):
    client.add_cog(utility(client))
