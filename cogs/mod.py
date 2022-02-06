import discord
from discord.ext import commands

class mod(commands.Cog):
    def __init__(self, LxBot):
        self.LxBot = LxBot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, user: discord.Member, role: discord.Role):
        try:
            await user.add_roles(role)
            await ctx.send(f"The role `{role}` was assigned to `{user}`")
        except Exception as e:
            await ctx.send("I do not have the necessary permissions to execute the command")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        try:
            await user.remove_roles(role)
            await ctx.send(f"The role `{role}` was removed from `{user}`")
        except Exception as e:
            await ctx.send("I do not have the necessary permissions to execute the command")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, userid: int, *, reason=None):
        if ctx.guild.get_member(userid) is not None:
            user = await self.LxBot.fetch_user(userid)
            await ctx.guild.kick(user, reason=reason)
            await ctx.send(f"Kicked {user.display_name}. Reason: {reason}")
        else:
            await ctx.send("User ID not found on server.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, userid: int, *, reason=None):
        if ctx.guild.get_member(userid) is not None:
            user = await self.LxBot.fetch_user(userid)
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Banned {user.display_name}. Reason: {reason}")
        else:
            await ctx.send(f"User ID not found on server.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userid: int, *, reason=None):
        user = await self.LxBot.fetch_user(userid)
        try:
            await ctx.guild.fetch_ban(user)
        except discord.NotFound:
            await ctx.send(f"{user.display_name} is not banned")
            return
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(f"Unbanned {user.display_name}. Reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=5):
        if amount in range(1, 16):
            deleted = await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f"Deleted `{len(deleted) - 1}` message(s)", delete_after=5)
        else:
            await ctx.send("You can't delete more than `1-15` message(s)", delete_after=5)


def setup(LxBot):
    LxBot.add_cog(mod(LxBot))