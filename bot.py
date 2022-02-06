import discord
import json
from discord.ext import commands

class HelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="LxBot Help", color=0x300c54)
        for cog, command in mapping.items():
            commands = [command.name for command in mapping[cog]]
            if commands:
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name == "nsfw" and not self.get_destination().is_nsfw():
                    embed.add_field(name=cog_name, value="NSFW-Commands only appear in NSFW-Channels", inline=False)    
                else:
                    embed.add_field(name=cog_name, value=", ".join(commands), inline=False)    
        embed.set_footer(text=f"Use help <module> to get information about that module.")
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title="LxBot Help", color=0x300c54)
        embed.add_field(name=cog.qualified_name, value='\n'.join([command.name for command in cog.get_commands()]))
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title="LxBot Help", color=0x300c54)
        embed.add_field(name=command.name, value=command.help)
        await self.get_destination().send(embed=embed)

async def getprefix(LxBot, message):
    with open("/data/bot/prefix.json") as json_stream:
        prefixes = json.load(json_stream)
    if prefixes.get(str(message.guild.id)): 
        return prefixes[str(message.guild.id)]
    else:
        return 'l!'

intents = discord.Intents.default()
intents.members = True
LxBot = commands.Bot(command_prefix = getprefix, help_command=HelpCommand(), intents=intents)
cogs = ["utility", "nsfw", "mod"]
for cog in cogs:
    LxBot.load_extension(f"cogs.{cog}")  

@LxBot.event
async def on_ready(): 
    print("Logged in as")
    print(f"Bot-Name: {LxBot.user.name} | {LxBot.user.id}")
    print(f"Discord Version: {discord.__version__}")

@LxBot.event
async def on_message(message):
    if message.guild != None:
        await LxBot.process_commands(message)
    else:
        pass

@LxBot.event
async def on_command_error(ctx, error):
    print(error)
    if hasattr(ctx.command, "on_error"):
        return
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown. Please try again after `{round(error.retry_after, 1)}` seconds.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing a required argument: `{error.param.name}`.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that argument.")
    elif isinstance(error, commands.NSFWChannelRequired):
        await ctx.send("Non-NSFW Channel detected!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have the required permissions")

@LxBot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix: str):
    with open("/data/bot/prefix.json") as json_stream:
        prefixes = json.load(json_stream)
    prefixes[str(ctx.guild.id)] = prefix
    with open("/data/bot/prefix.json", "w") as json_stream:
        json.dump(prefixes, json_stream, indent=4)
    await ctx.send(f"Prefix was changed to ``{prefix}``")

LxBot.run("Your Token")