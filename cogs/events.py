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
############################# INFOS ############################
    @commands.command(aliases=['i'])
    async def infos(self,ctx,*suggestion):
        embed=discord.Embed(description="Hyperfort est un bot créé par <@175236651734269952> \n **__Commandes__** Voici les commandes qui sont à votre disposition : ", color=0xf8e71c)
        embed.add_field(name=";infos\nalias ;i", value="*Renvoie des infos sur le bot et comment l'utiliser*",inline=True)
        embed.add_field(name=";etirer [texte]\nalias ;et", value="*Renvoie votre texte avec des espaces entre chaque\nl e t t r e*",inline=True)
        embed.add_field(name=";question [question]\nalias ;q", value="*Répond à votre question par :\noui/non/possible/tg*",inline=True)
        embed.add_field(name=";suggest[suggestion] \nalias ;sg", value="*Renvoie votre suggestion avec les réactions :arrow_up_small: :arrow_down_small: pour permettre de voter*", inline=True)
        embed.add_field(name=";reactionmessage \nalias ;rm", value="*Vous permet de créer différentes choses interactivement* \n ``réservé aux admins``", inline=True)
        embed.add_field(name="**__GitHub__**", value="Retrouvez son code source ici : https://github.com/Hypermario/TUMO-bot", inline=False)
        await ctx.send(embed=embed)
####################################################################################
#----------------------------------------------------------------------------------------------
############################# SUGGESTION ############################
    @commands.command(aliases=['sg'])
    async def suggest(self,ctx,*suggestion):
        await ctx.message.delete(delay=5.0)      # à laisser (?)
        
        if (not suggestion):
            await ctx.send('Pense à me donner ta suggestion', delete_after=10)
        else:
            setup=discord.Embed(title=" ".join(suggestion),colour=discord.Colour.gold())
            setup.set_author(name=f'{ctx.author} suggère :', icon_url=f'{ctx.author.avatar_url}')
            setupMessage = await ctx.send(embed=setup)    
            await setupMessage.add_reaction('🔼')
            await setupMessage.add_reaction('🔽')
            logging.warning("exec Sg pour : "+" ".join(suggestion))
####################################################################################
#----------------------------------------------------------------------------------------------
############################# E T I R E U R   D E   T E X T E ############################
    @commands.command(aliases=['et'])
    async def etirer(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        await ctx.send(" ".join(texte))
        logging.warning("exec Et pour : "+" ".join(texte))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ SETUP ############################
def setup(client):
    client.add_cog(Events(client))
####################################################################################
