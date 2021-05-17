import discord
import json
import asyncio
import logging
from discord.ext import commands

class Textransform(commands.Cog):

    def __init__(self, client):
        logging.basicConfig(filename='logs.log', format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y | %H:%M:%S]')
        self.client = client

#----------------------------------------------------------------------------------------------
############################# E T I R E U R   D E   T E X T E ############################
    @commands.command(aliases=['et'])
    async def etirer(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        await ctx.send(" ".join(texte))
        logging.warning("exec Et pour : "+" ".join(texte))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ BULLES TEXTE ############################
    @commands.command(aliases=['ar'])
    async def arrondir(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        chars = '🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩'
        final = []
        for mot in texte:
            for lettres in mot:
                if lettres.isalpha():
                    index = ord(lettres)-ord('a')
                    final.append(chars[index])
                else:
                    final.append(lettres)
        await ctx.send(" ".join(final))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ CARRE TEXTE ############################
    @commands.command(aliases=['c'])
    async def carre(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        chars = '🄰🄱🄲🄳🄴🄵🄶🄷🄸🄹🄺🄻🄼🄽🄾🄿🅀🅁🅂🅃🅄🅅🅆🅇🅈🅉'
        final = []
        for mot in texte:
            for lettres in mot:
                if lettres.isalpha():
                    index = ord(lettres)-ord('a')
                    final.append(chars[index])
                else:
                    final.append(lettres)
        await ctx.send(" ".join(final))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ MINUSCULES TEXTE ############################
    @commands.command(aliases=['min'])
    async def minuscule(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        chars = 'abcdefghijklmnopqrstuvwxyz'
        final = []
        for mot in texte:
            for lettres in mot:
                if lettres.isalpha():
                    index = ord(lettres)-ord('a')
                    final.append(chars[index])
                else:
                    final.append(lettres)
        await ctx.send("".join(final))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ MAJUSCULES TEXTE ############################
    @commands.command(aliases=['maj'])
    async def majuscule(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        final = []
        for mot in texte:
            for lettres in mot:
                if lettres.isalpha():
                    index = ord(lettres)-ord('a')
                    final.append(chars[index])
                else:
                    final.append(lettres)
        await ctx.send("".join(final))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ EMOJIS TEXTE ############################
    @commands.command(aliases=['em'])
    async def emoji(self,ctx,*,texte):
        await ctx.message.delete(delay=5.0)
        chars = ':regional_indicator_a:',':regional_indicator_b:',':regional_indicator_c:',':regional_indicator_d:',':regional_indicator_e:',':regional_indicator_f:',':regional_indicator_g:',':regional_indicator_h:',':regional_indicator_i:',':regional_indicator_j:',':regional_indicator_k:',':regional_indicator_l:',':regional_indicator_m:',':regional_indicator_n:',':regional_indicator_o:',':regional_indicator_p:',':regional_indicator_q:',':regional_indicator_r:',':regional_indicator_s:',':regional_indicator_t:',':regional_indicator_u:',':regional_indicator_v:',':regional_indicator_w:',':regional_indicator_x:',':regional_indicator_y:',':regional_indicator_z:',
        final = []
        for mot in texte:
            for lettres in mot:
                if lettres.isalpha():
                    index = ord(lettres)-ord('a')
                    final.append(chars[index])
                else:
                    final.append(lettres)
        await ctx.send(" ".join(final))
####################################################################################
#----------------------------------------------------------------------------------------------
############################ SETUP ############################
def setup(client):
    client.add_cog(Textransform(client))
####################################################################################
