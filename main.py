import discord
import os
import json
import logging
from discord.ext import commands, tasks

logging.basicConfig(filename='logs.log', format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y | %H:%M:%S]')
############################ PREFIX ############################
def get_prefix(client, message):
    with open('infos.json', 'r') as f:
        data = json.load(f)

    try:
        return data[str(message.guild.id)]['general']['prefix']
    except (AttributeError, TypeError):
        return '>'

try:
    client = commands.Bot(command_prefix = get_prefix)
    client.remove_command("help")
except (AttributeError, TypeError):
    pass
####################################################################################
#----------------------------------------------------------------------------------------------
############################ ON GUILD EVENT ############################
@client.event
async def on_guild_join(guild):
    with open('infos.json', 'r') as f:
        data = json.load(f)
    data[str(guild.id)] = {
        
        "general": {
            "name": str(guild.name),
            "lang": "fr",
            "prefix": ";",
            "aoStatusChannel": None
        },
        "recrut": {
            "message": None,
            "logs": None,
            "category": None,
            "recrutRole": None,
            "applyRole": None,
            "memberRole": None
        },
        "rm": {},
        "channels": {}
    }
    
    with open('infos.json', 'w') as f:
        json.dump(data, f, indent=4)
    logging.warning(f'HYPERFORT est arrivé sur {guild.name} !')
      
@client.event
async def on_guild_remove(guild):
    with open('infos.json', 'r') as f:
        data = json.load(f)

    data.pop(str(guild.id))

    with open('infos.json', 'w') as f:
        json.dump(data, f, indent=4)
    logging.warning(f'HYPERFORT est parti de {guild.name}')
####################################################################################
#----------------------------------------------------------------------------------------------
############################# PREFIX COMMAND ############################
@client.command()
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('infos.json', 'r') as f:
        data = json.load(f)

    data[str(ctx.guild.id)]['general']['prefix'] = prefix

    with open('infos.json', 'w') as f:
        json.dump(data, f, indent=4)

    await ctx.send(f'Prefix changé en : {prefix}')
    logging.warning(f'Prefix changé en : {prefix} pour {ctx.guild.name}')
####################################################################################
#----------------------------------------------------------------------------------------------
############################ ERRORS ############################
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        return 0
    elif isinstance(error, commands.CommandNotFound):
        return 0
    else:
        errorChannel = client.get_channel(664926718762418226)
        await errorChannel.send(f"```py\n{str(error)}```")
        logging.warning(str(error))
        return print(error)
####################################################################################
#----------------------------------------------------------------------------------------------
############################ LOAD FUNCTION ############################
hypermario = 175236651734269952
@client.command()
async def leave(ctx, guild_id):
    if(ctx.author.id == hypermario):
        guild = discord.utils.find(lambda g: g.id == int(guild_id), client.guilds)
        await guild.leave()
        with open('infos.json', 'r') as f:
            data = json.load(f)

        data.pop(str(guild.id))

        with open('infos.json', 'w') as f:
            json.dump(data, f, indent=4)
        logging.warning(f'HYPERFORT est parti de {guild.name}')
        await ctx.send(f'{guild.name} left')

@client.command()
async def load(ctx, extension):
    if(ctx.author.id == hypermario):
        client.load_extension(f'cogs.{extension}')
        logging.warning(f'{extension} loaded')
        await ctx.send(f'{extension} loaded')

@client.command()
async def reload(ctx, extension):
    if(ctx.author.id == hypermario):
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        logging.warning(f'{extension} reloaded')
        await ctx.send(f'{extension} reloaded')

@client.command()
async def unload(ctx, extension):
    if(ctx.author.id == hypermario):
        client.unload_extension(f'cogs.{extension}')
        logging.warning(f'{extension} unloaded')
        await ctx.send(f'{extension} unloaded')

with open('logs.log', 'w'):
    pass
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        logging.warning(f'{filename} loaded')
        client.load_extension(f'cogs.{filename[:-3]}')
####################################################################################
#----------------------------------------------------------------------------------------------
client.run('#####')
#----------------------------------------------------------------------------------------------