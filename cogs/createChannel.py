import discord
import json
import logging
from discord.ext import commands

class createChannel(commands.Cog):

    def __init__(self, client):
        logging.basicConfig(filename='logs.log', format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y | %H:%M:%S]')
        self.client = client
        self.hypermario = 175236651734269952

    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_channels=True)
    async def on_voice_state_update(self, member, before, after):
        if(after.channel is not before.channel):                
            if(before.channel is not None and len(before.channel.members) == 0):
                guild = member.guild
                with open('infos.json', 'r') as f:
                    data = json.load(f)
                    
                for channel_id in data[str(guild.id)]["channels"].keys():
                    try:
                        createdChannels = data[str(guild.id)]['channels'][channel_id]['created']
                    except KeyError:
                        continue
                    else:
                        if(before.channel.id in createdChannels):
                            await before.channel.delete()

                            createdChannels.remove(before.channel.id)
                            
                            with open('infos.json', 'w') as f:
                                json.dump(data, f, indent=4)
                            break
            
            if(after.channel is not None):
                guild = member.guild
                with open('infos.json', 'r') as f:
                    data = json.load(f)
                    
                try:
                    channel_id = str(after.channel.id)
                    channelName = data[str(guild.id)]['channels'][channel_id]['name']
                    createdChannels = data[str(guild.id)]['channels'][channel_id]['created']
                except KeyError:
                    return
                else:
                    if("{num}" in channelName):
                        num = len(createdChannels)+1
                    if("{name}" in channelName):
                        name = member.display_name
                        
                    try:
                        newChannelName = str(eval(f'f"""{channelName}"""'))
                    except NameError:
                        newChannelName = 'ARGUMENT ERROR'
                    finally:
                        newChannel = await after.channel.clone(name=newChannelName)
                        await member.move_to(newChannel)
                        
                        data[str(guild.id)]['channels'][channel_id]['created'].append(newChannel.id)
                        
                        with open('infos.json', 'w') as f:
                            json.dump(data, f, indent=4)
                    return
            
    @commands.command(aliases=['cc'])
    @commands.has_permissions(manage_channels=True)
    async def createchannel(self, ctx, channel_id=None, *, name=None):
        setup = discord.Embed(colour=discord.Colour.gold())
        if(channel_id is not None and name is not None):
            with open('infos.json', 'r') as f:
                data = json.load(f)
            try:
                channel = self.client.get_channel(int(channel_id))
            except TypeError:
                setup.set_author(name=f"Tu dois renseigner un id de channel correct ! Regarde `{ctx.prefix}help createchannel` pour obtenir de l'aide")
            else:
                if(name == 'remove' or name == 'delete'):
                    data[str(ctx.guild.id)]['channels'].pop(str(channel_id))
                    
                    with open('infos.json', 'w') as f:
                        json.dump(data, f, indent=4)
                
                    setup.set_author(name=f"**{channel.name}** n'est plus un channel dynamique !")
                    logging.warning(f'removed dynamic channel {ctx.guild.name}')
                
                elif(channel is not None and str(channel.type) == "voice"):
                    
                    data[str(ctx.guild.id)]['channels'][str(channel_id)] = {
                        "name": str(name),
                        "created": []
                        }
                    
                    with open('infos.json', 'w') as f:
                        json.dump(data, f, indent=4)
                    
                    setup.set_author(name=f"**{channel.name}** est enregistré comme channel dynamique !")
                    logging.warning(f'added dynamic channel {ctx.guild.name}')
                else:
                    setup.set_author(name="Ce channel n'existe pas ou n'est pas du bon type")
        else:
            setup.set_author(name=f"Tu dois renseigner un id de channel et un nom pour le channel ! Regarde {ctx.prefix}help createchannel pour obtenir de l'aide")
        
        return await ctx.send(embed=setup)
    
def setup(client):
    client.add_cog(createChannel(client))