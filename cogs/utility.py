import discord
import random
import nekos
from discord.ext import commands

class utility(commands.Cog):
    def __init__(self, LxBot):
        self.LxBot = LxBot

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question: str):
        answer = random.choice(["yes", "definitely yes", "no", "definitely no", "maybe", "i dont know", "why you asking me this?", "who knows", "ask me again later"])
        embed = discord.Embed(title="8ball", description=f"**Question:** {question} \n **Answer:** {answer}", color=0x300c54)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Question asked by {ctx.author.display_name}.")
        await ctx.send(embed=embed)

    @commands.command()
    async def owoify(self, ctx, *, text: str):
        try:
            await ctx.send(nekos.owoify(text))
        except Exception as owo:
            await ctx.send(owo)
        
    @commands.command()
    async def avatar(self, ctx, user: discord.Member):
        embed = discord.Embed(title=f"Avatar of {user.display_name}", color=0x300c54)
        embed.set_image(url=user.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Avatar requested by {ctx.author.display_name}.")
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(color=0x300c54)
        embed.add_field(name="Name", value=f"{ctx.guild.name} \n ({ctx.guild.id})")
        embed.add_field(name="Owner", value=ctx.guild.owner)
        embed.add_field(name="Created at", value=ctx.guild.created_at.__format__('%A, %d. %B %Y'))
        embed.add_field(name="Channels", value=f"Text Channels: **{len(ctx.guild.text_channels)}**\nVoice Channels: **{len(ctx.guild.voice_channels)}**\nCategories: **{len(ctx.guild.categories)}**\nAFK Channel: {ctx.guild.afk_channel}")
        embed.add_field(name=f"Roles", value=len(ctx.guild.roles))
        embed.add_field(name="Member Count", value=ctx.guild.member_count)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Information requested by {ctx.author.display_name}.")
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member):
        roles = [role.name for role in user.roles if role.name != "@everyone"]
        embed = discord.Embed(color=0x300c54)
        embed.add_field(name="Name", value=f"{user.display_name}\n({user.id})", inline=False)
        embed.add_field(name="Discriminator", value=f"#{user.discriminator}", inline=False)
        embed.add_field(name="Bot", value=user.bot, inline=False)
        if len(roles) != 0:
            embed.add_field(name=f"Roles ({len(roles)})", value=', '.join(roles), inline=False)
        embed.add_field(name="Joined at", value=user.joined_at.__format__('%A, %d. %B %Y'), inline=False)
        embed.add_field(name="Created at", value=user.created_at.__format__('%A, %d. %B %Y'), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Information requested by {ctx.author.display_name}.")
        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self, ctx, userid: int):
        try:
            embed = discord.Embed(color=0x300c54)
            user = await self.LxBot.fetch_user(userid)
            embed.add_field(name="Name", value=f"{user.display_name}\n({user.id})", inline=False)
            embed.add_field(name="Discriminator", value=f"#{user.discriminator}", inline=False)
            embed.add_field(name="Bot", value=user.bot, inline=False)
            embed.add_field(name="Created at", value=user.created_at.__format__('%A, %d. %B %Y'), inline=False)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Information requested by {ctx.author.display_name}.")
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("Unknown User ID.")
        
def setup(LxBot):
    LxBot.add_cog(utility(LxBot))