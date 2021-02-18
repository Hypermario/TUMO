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
        await self.client.change_presence(status=discord.Status.dnd, activity=None)
        channel = self.client.get_channel(636029798468157441)
        await channel.send("Je suis en ligne !")
        logging.warning('----- ready -----')
####################################################################################
############################ QUESTION ############################
    @commands.command(aliases=['q'])
    async def question(self, ctx, *, question):
        responses=['tg', 'oui', 'non', 'possible']
        await ctx.send(f'Question: {question}\nRéponse: {random.choice(responses)}')
        logging.warning(f'exec Q pour {question}')
####################################################################################
#----------------------------------------------------------------------------------------------
############################ SETUP ############################
def setup(client):
    client.add_cog(Events(client))
####################################################################################
