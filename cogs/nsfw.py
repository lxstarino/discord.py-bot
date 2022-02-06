import discord
import nekos
from discord.ext import commands

class nsfw(commands.Cog):
    def __init__(self, LxBot):
        self.LxBot = LxBot

    @commands.command()
    @commands.is_nsfw()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hentai(self, ctx, endpoint: str="", amount: int=1):
        if "cooldownbypass" in str(ctx.author.roles):
            self.hentai.reset_cooldown(ctx)
        try:
            if amount in range(1, 4):
                for _ in range(amount):
                    img_infos = nekos.nsfwimg(endpoint)
                    embed = discord.Embed(title=f"NSFW - {img_infos[1]}", url=img_infos[0], color=0x300c54)
                    embed.set_image(url=img_infos[0])
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Image requested by {ctx.author.display_name}.")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="NSFW - Error", description="You can't request more than 3 images.", color=0x300c54)
                await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="NSFW - Error", description=e, color=0x300c54)
            await ctx.send(embed=embed)

def setup(LxBot):
    LxBot.add_cog(nsfw(LxBot))