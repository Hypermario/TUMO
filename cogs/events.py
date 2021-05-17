import discord
import random
import logging
from discord.ext import commands

class Events(commands.Cog):

    logging.basicConfig(filename='logs.log', format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y | %H:%M:%S]')
    def __init__(self, client):
        self.client = client
        self.hypermario = 175236651734269952

#----------------------------------------------------------------------------------------------
############################ ON READY ############################
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.online, activity=None)
        channel = self.client.get_channel(636029798468157441)
        if not channel:
            pass
        else:
            await channel.send("Je suis en ligne !")
        logging.warning('----- ready -----')
####################################################################################

############################ SETUP ############################
def setup(client):
    client.add_cog(Events(client))
####################################################################################