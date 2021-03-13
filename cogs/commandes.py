import discord
import random
import time
import json
import asyncio
import logging
from discord.ext import commands

class Commandes(commands.Cog):

    logging.basicConfig(filename='logs.log', format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y | %H:%M:%S]')
    def __init__(self, client):
        self.client = client

##### CLEAR
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        await ctx.channel.purge(limit=amount)
        logging.warning(f'Deleted {amount} messages in {ctx.message.channel}')
        
##### HYPER CLEAR/DELETE        
    @commands.command(aliases=['hclear', 'hyclear'])
    async def hyperclear(self, ctx, amount=0):
        hypermario = 175236651734269952
        handjaye = 175236722098044928
        if(ctx.author.id == handjaye or ctx.author.id == hypermario):
            await ctx.channel.purge(limit=amount)
            logging.warning(f'Deleted {amount} messages in {ctx.message.channel}')
            
    @commands.command(aliases=['hdel', 'hydelete', 'hdelete'])
    async def hyperdelete(self, ctx, message_id : int, channel=0):
        hypermario = 175236651734269952
        handjaye = 175236722098044928
        if(ctx.author.id == handjaye or ctx.author.id == hypermario):
            if(channel == 0):
                message = await ctx.channel.fetch_message(message_id)
            else:
                channel = self.client.get_channel(channel)
                if(channel is not None):
                    message = await channel.fetch_message(message_id)
                else:
                    return
            await message.delete()
            await ctx.message.delete()
            logging.warning(f'Deleted {message.content} in {ctx.message.channel}')

##### SPAM
    @commands.command()
    async def spam(self, ctx, times=1, name='@everyone', ):
        handjaye = 175236722098044928
        hypermario = 175236651734269952
        await ctx.message.delete()
        if(ctx.author.id == handjaye or ctx.author.id == hypermario):
            for loop in range(times):
                await ctx.send(name)
                time.sleep(0.5)
            logging.warning(f'exec spam {times}')

############################ QUESTION ############################
    @commands.command(aliases=['q'])
    async def question(self, ctx, *, question):
        responses=['tg', 'oui', 'non', 'possible']
        if("la vie" in question or "life" in question or "univers" in question):
            await ctx.send(f'Question: {question}\nRéponse: 42.')
        else:
            await ctx.send(f'Question: {question}\nRéponse: {random.choice(responses)}.')
        logging.warning(f'exec Q pour {question}')
####################################################################################

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx):
        channel = ctx.message.author.voice.channel
        if(channel is None): return
        
        voice = ctx.message.author.voice
        everyone = ctx.guild.default_role
        
        await channel.set_permissions(everyone, speak = False, read_messages = False, connect=False, use_voice_activation = False)
        
        for member in channel.members:
            memberPerms = member.permissions_in(channel)
            if(memberPerms.mute_members == False and memberPerms.priority_speaker == False):
                if(member.voice.self_mute == False and member.voice.mute == False):
                    await member.edit(mute=True)
                    
        await ctx.send('mute')
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx):
        channel = ctx.message.author.voice.channel
        if(channel is None): return
        
        voice = ctx.message.author.voice
        everyone = ctx.guild.default_role
        
        await channel.set_permissions(everyone, speak = True, read_messages = False, connect=False, use_voice_activation = True)
        
        for member in channel.members:
            memberPerms = member.permissions_in(channel)
            if(memberPerms.mute_members == False and memberPerms.priority_speaker == False):
                if(member.voice.self_mute == False and member.voice.mute == True):
                    await member.edit(mute=False)
                    
        await ctx.send('unmute')

    @commands.command()
    async def help(self, ctx, categorie=''):
        categorie = categorie.lower()
        prefix = ctx.prefix
        
        embed = discord.Embed(colour = discord.Colour.gold())

        if(categorie == 'clear'):
            embed.set_author(name='Help Clear')
            embed.add_field(name=f'**{prefix}clear <montant>**', value='*Supprime un nombre de messages donné dans le channel.*\n\n__La permission : gérer les messages est necessaire.__')
        
        elif(categorie == 'question'):
            embed.set_author(name='Help Question')
            embed.add_field(name=f'**{prefix}question <question>**', value='*Le bot répondra à ta question en te disant la vérité vraie.*')

        elif(categorie == 'recrutement'):
            embed.set_author(name='Help Recrutement')
            embed.add_field(name=f'**{prefix}recrutement <commande>**', value="**message**\n*Crée un message où reagir pour les joueurs qui souhaitent rejoindre la guilde.*\n\n**applyrole**\n*Défini le role qu'auront les joueurs en réagisant au message.*\n\n**recrutrole**\n*Défini le role des recruteurs (pour la permission de voir les réponses).*\n\n**category**\nCrée la categorie ou les channels réponses se créeront.*\n\n**questions**\n*Défini les questions pour votre recrutement (20 max).*\n\n**logs**\n*Défini le channel de logs des réponses recrutement et les questions qui y seront stockés.*\n\nNécessite le role Officier.")

        elif(categorie == 'createchannel' or categorie == 'cc'):
            embed.set_author(name='Help CreateChannel')
            embed.add_field(name=f'**{prefix}createchannel <channel_id> <nom OU delete>**', value="**<channel_id>**\n*L'id du channel, vous pouvez l'avoir en activant le mode developpeur dans : Parametres -> Apparence, clique droit sur le channel voulu -> Copier l'identifiant.*\n\n**<nom OU remove>**\n*<nom> Défini le nom du channel, vous pouvez ajouter les arguments suivants dans le nom de votre channel a creer :\n----{name}: le nom du créateur du channel;\n----{num}: le numéro du channel.*\n\n*<remove> Le channel choisi ne sera plus dynamique.*\n\nNécecite la permission de gerer les channels")
        elif('reactionmessage' in categorie or categorie == 'rm'):
            embed.set_author(name='Help ReactionMessage')
            embed.add_field(name=f'**{prefix}rm <prefaits>**', value="Vous aurez le choix entre deux type de reaction message :\n---0️⃣ pour lister sur le message les membres qui ont réagi\n---1️⃣ pour donner un role aux membres qui ont réagi\n\n**<prefaits>**\nMettez le nom d'un reactionMessage préfait (non obligatoire):\n---battle : crée une bataille rapidement qui liste vos joueurs sur le message")
        
        else:
            embed.set_author(name='Help')
            embed.add_field(name="Clear", value='*Supprime un nombre de messages donné.*', inline=True)
            embed.add_field(name="Question", value='*Pose une question et le bot te repondera.*', inline=True)
            embed.add_field(name="Recrutement", value='*Permet de gérer le recrutement.*', inline=True)
            embed.add_field(name="CreateChannel", value='*Permet de faire des channels qui se créent et se supprime automatiquement.*', inline=True)
            embed.add_field(name="ReactionMessage", value="*Permet de créer des messages avec des reactions utiles.*")
            embed.add_field(name=f"{prefix}hgtimers", value="*Permet de gérer le channel de l'hellgate timers.*", inline=True)
            embed.add_field(name=f"{prefix}help <commande>", value="*Permet d'en savoir plus sur la commande donnée.*", inline=False)
            embed.add_field(name="Rejoignez le discord !", value="https://discord.gg/gMeHW8G", inline=False)
            
        await ctx.send(embed=embed)
        
        
def setup(client):
    client.add_cog(Commandes(client))
