import discord
import json
import asyncio
import logging
from discord.ext import commands

class rMessage(commands.Cog):

    def __init__(self, client):
        logging.basicConfig(filename='logs.log', format='%(asctime)s %(message)s', datefmt='[%d/%m/%Y | %H:%M:%S]')
        self.client = client
        self.hypermario = 175236651734269952
    
    @commands.command(aliases=['rm'])
    @commands.has_permissions(manage_messages=True)
    async def reactionmessage(self, ctx, premade='no'):
        if(str(ctx.channel.type) == 'text'):
            with open('infos.json', 'r') as f:
                data = json.load(f)
            if(premade == 'no'):
                await ctx.message.delete()
                setup = discord.Embed(colour=discord.Colour.lighter_gray())
                setup.set_author(name="A quoi servira ce message reaction ?")
                setup.add_field(name="- 0️⃣ pour donner un role;", value="\u200b", inline=False)
                setup.add_field(name="- 1️⃣ pour lister les membres qui ont réagi;", value="\u200b", inline=False)
                setup.add_field(name="- 2️⃣ pour faire un système de score;", value="\u200b", inline=False)
                setup.set_footer(text="❌ pour annuler.")
                setupMessage = await ctx.send(embed=setup)

                await setupMessage.add_reaction('0️⃣')
                await setupMessage.add_reaction('1️⃣')
                await setupMessage.add_reaction('2️⃣')
                await setupMessage.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.author
                
                try:                    
                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await setupMessage.delete()
                    return await ctx.send(f"Tu n'as pas répondu assez vite !", delete_after=10.0)
                else:
                    setup.clear_fields()
                    setup.set_footer(text="")
                    await setupMessage.clear_reactions()
#######################################################################################

################################ REACTION ROLE SETUP ################################
                    if(reaction.emoji == '0️⃣'):
                        emojis = list()
                        roles = list()
                        
                        def check(m):
                            return m.author == ctx.message.author and m.channel == ctx.channel
                                        
############################# CHANNEL
                        setup.set_author(name="Mentionnez le channel où sera affiché le message")
                        await setupMessage.edit(embed=setup)
                        
                        channelMention = await self.client.wait_for('message', timeout=60.0, check=check)
                        repChannel = ctx.guild.get_channel(channelMention.raw_channel_mentions[0])
                        await channelMention.delete()
                        
                        if(repChannel is not None):
################################# MESSAGE
                            setup.set_author(name="Quel sera le message affiché ?")
                            await setupMessage.edit(embed=setup)

                            rmContent = await self.client.wait_for('message', timeout=60.0, check=check)
                            messageContent = str(rmContent.content)
                            await rmContent.delete()

                            for loop in range(20):
                                try:
######################################### EMOJI
                                    def check(reaction, user):
                                        return user == ctx.author
                                    
                                    await setupMessage.clear_reactions()
                                    setup.set_author(name=f"Réagissez sur ce message avec un emoji (plus que {20-loop} emojis)")
                                    await setupMessage.edit(embed=setup)
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                                    if(reaction.emoji != '❌'):
                                        emojis.append(reaction.emoji)

                                        def check(m):
                                            return m.author == ctx.message.author and m.channel == ctx.channel
                                        
############################################# ROLE
                                        setup.set_author(name="Mentionnez le role qui sera attribué pour cet emoji")
                                        await setupMessage.edit(embed=setup)
                                        
                                        roleMention = await self.client.wait_for('message', timeout=60.0, check=check)
                                        roles.append(roleMention.raw_role_mentions[0])
                                        await roleMention.delete()
                                except asyncio.TimeoutError:
                                    await setupMessage.delete()
                                    return await ctx.send("Tu n'as pas répondu assez vite !", delete_after=10.0)
                                else:
                                    await setupMessage.clear_reactions()
######################################### CONTINUER ?
                                    setup.set_author(name=f"Voulez vous ajouter un autre emoji role à ce message ? (plus que {20-loop} emojis)")
                                    await setupMessage.edit(embed=setup)
                                    await setupMessage.add_reaction('☑️')
                                    await setupMessage.add_reaction('❌')
                                    
                                    def check(reaction, user):
                                        return user == ctx.author
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                                    if(reaction.emoji == '❌'):
                                        break
                                    elif(reaction.emoji == '☑️'):
                                        continue

################################# FIN (ENVOI DU MESSAGE ET ENREGISTREMENT)
                            await setupMessage.clear_reactions()
                            rmMessageEmbed = discord.Embed(colour=discord.Colour.lighter_gray())
                            rmMessageEmbed.set_author(name=messageContent)
                            #rmMessageEmbed.set_thumbnail(url=ctx.guild.icon_url)
                            rmMessage = await repChannel.send(embed=rmMessageEmbed)
                            
                            data[str(ctx.guild.id)]['rm'][str(rmMessage.id)] = {
                                "type": 0
                            }
                            for index, emoji in enumerate(emojis):
                                data[str(ctx.guild.id)]['rm'][str(rmMessage.id)][str(emoji)] = roles[index]
                                await rmMessage.add_reaction(emoji)
                            
                            with open('infos.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                
                            logging.warning(f'new rM role in {ctx.guild.name}')
                            setup.set_author(name="Envoyé !")
                            await setupMessage.edit(embed=setup)
                            await setupMessage.delete(delay=5.0)
                        else:
                            return await ctx.send("Ce channel n'existe pas!")
#######################################################################################

################################ REACTION LIST SETUP ################################
                    elif(reaction.emoji == '1️⃣'):
                        emojis = list()
                        category = list()
                        
                        def check(m):
                            return m.author == ctx.message.author and m.channel == ctx.channel
                                        
############################# CHANNEL
                        setup.set_author(name="Mentionnez le channel où sera affiché le message")
                        await setupMessage.edit(embed=setup)
                        
                        channelMention = await self.client.wait_for('message', timeout=60.0, check=check)
                        repChannel = ctx.guild.get_channel(channelMention.raw_channel_mentions[0])
                        await channelMention.delete()
                        
                        if(repChannel is not None):
################################# MESSAGE
                            setup.set_author(name="Quel sera le message principal affiché ?")
                            await setupMessage.edit(embed=setup)

                            rmContent = await self.client.wait_for('message', timeout=60.0, check=check)
                            messageContent = str(rmContent.content)
                            await rmContent.delete()

                            for loop in range(20):
                                try:
######################################### EMOJI
                                    def check(reaction, user):
                                        return user == ctx.author
                                    
                                    await setupMessage.clear_reactions()
                                    setup.set_author(name=f"Réagissez sur ce message avec un emoji (plus que {20-loop} emojis)")
                                    await setupMessage.edit(embed=setup)
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                                    emojis.append(reaction.emoji)

                                    def check(m):
                                        return m.author == ctx.message.author and m.channel == ctx.channel
                                    
######################################### CATEGORIE
                                    setup.set_author(name="Ecrivez un nom de categorie pour l'emoji choisi")
                                    setup.add_field(name="Vous pouvez ajouter l'argument {num} pour afficher le nombre de personnes d'une categorie", value="\u200b")
                                    await setupMessage.edit(embed=setup)
                                    
                                    categoryName = await self.client.wait_for('message', timeout=60.0, check=check)
                                    category.append(str(categoryName.content))
                                    await categoryName.delete()
                                except asyncio.TimeoutError:
                                    await setupMessage.delete()
                                    return await ctx.send("Tu n'as pas répondu assez vite !", delete_after=10.0)
                                else:
                                    await setupMessage.clear_reactions()
                                    setup.clear_fields()
######################################### CONTINUER ?
                                    setup.set_author(name=f"Voulez vous ajouter un autre emoji -> categorie à ce message ? (plus que {20-loop} emojis)")
                                    await setupMessage.edit(embed=setup)
                                    await setupMessage.add_reaction('☑️')
                                    await setupMessage.add_reaction('❌')
                                    
                                    def check(reaction, user):
                                        return user == ctx.author
                                    
                                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                                    if(reaction.emoji == '❌'):
                                        break
                                    elif(reaction.emoji == '☑️'):
                                        continue

################################# ENVOI DU MESSAGE
                            await setupMessage.clear_reactions()
                            rmMessageEmbed = discord.Embed(colour=discord.Colour.lighter_gray())
                            rmMessageEmbed.set_author(name=messageContent)
                            #rmMessageEmbed.set_thumbnail(url=ctx.guild.icon_url)

                            for index, categories in enumerate(category):
                                if("{num}" in categories):
                                    num = 0
                                    newListName = str(eval(f'f"""{categories}"""'))
                                else:
                                    newListName = categories
                                rmMessageEmbed.add_field(name=newListName, value="\u200b")
                                
                            
                            rmMessage = await repChannel.send(embed=rmMessageEmbed)
################################# ENREGISTREMENT
                            data[str(ctx.guild.id)]['rm'][str(rmMessage.id)] = {
                                "type": 1
                            }
                            for index, emoji in enumerate(emojis):
                                data[str(ctx.guild.id)]['rm'][str(rmMessage.id)][str(emoji)] = [index, category[index]]
                                await rmMessage.add_reaction(emoji)
                            
                            with open('infos.json', 'w') as f:
                                json.dump(data, f, indent=4)
                            
                            logging.warning(f'new rM category in {ctx.guild.name}')
                            setup.set_author(name="Envoyé !")
                            await setupMessage.edit(embed=setup)
                            await setupMessage.delete(delay=10.0)
                        else:
                            return await ctx.send("Ce channel n'existe pas!")
#######################################################################################

################################ COUNTER SETUP ################################
                    elif(reaction.emoji == '2️⃣'):
                        
                        def check(m):
                            return m.author == ctx.message.author and m.channel == ctx.channel
                                        
############################# CHANNEL
                        setup.set_author(name="Mentionnez le channel où sera affiché le message")
                        await setupMessage.edit(embed=setup)
                        
                        channelMention = await self.client.wait_for('message', timeout=60.0, check=check)
                        repChannel = ctx.guild.get_channel(channelMention.raw_channel_mentions[0])
                        await channelMention.delete()
                        
                        if(repChannel is not None):
################################# MESSAGE
                            setup.set_author(name="Quel sera le message affiché ?")
                            await setupMessage.edit(embed=setup)

                            rmContent = await self.client.wait_for('message', timeout=60.0, check=check)
                            messageContent = str(rmContent.content)
                            await rmContent.delete()
                            await setupMessage.clear_reactions()
                                                    
################################# ENVOI
                            rmMessageEmbed = discord.Embed(colour=discord.Colour.lighter_gray())
                            rmMessageEmbed.set_author(name=messageContent)
                            #rmMessageEmbed.set_thumbnail(url=ctx.guild.icon_url)
                            rmMessageEmbed.add_field(name='0', value="\u200b")
                            rmMessage = await repChannel.send(embed=rmMessageEmbed)
                            
                            await rmMessage.add_reaction('⬆️')
                            await rmMessage.add_reaction('⬇️')                            
################################# ENREGISTREMENT
                            data[str(ctx.guild.id)]['rm'][str(rmMessage.id)] = {
                                "number": 0,
                                "type": 2
                            }
                            with open('infos.json', 'w') as f:
                                json.dump(data, f, indent=4)
                                
                            setup.set_author(name='Envoyé!')
                            await setupMessage.edit(embed=setup)
                            await setupMessage.delete(delay=10.0)
                            logging.warning(f'rM counter created in {ctx.guild.name}')
                        else:
                            return await ctx.send("Ce channel n'existe pas!")
################################ CANCEL SETUP ################################
                    elif(reaction.emoji == '❌'):
                        await setupMessage.delete()
                        return await ctx.send("Commande annulée", delete_after=5.0)
#######################################################################################

################################ BATTLE SETUP ################################
            elif(premade == 'battle'):
                setup = discord.Embed(colour=discord.Colour.lighter_gray())
                setup.set_author(name="Mentionnez le channel où le message sera affiché")
                setup.set_footer(text="Ecrivez 'cancel' pour annuler")
                setupMessage = await ctx.send(embed=setup)
                
                try:
                    def check(m):
                        return m.author == ctx.message.author and m.channel == ctx.channel
                    
                    channelMention = await self.client.wait_for('message', timeout=60.0, check=check)
                    
                    if(channelMention.content != 'cancel'):
                        repChannel = self.client.get_channel(channelMention.raw_channel_mentions[0])
                        if(repChannel is not None):
                            setup.set_author(name="Quel sera le nom de la battle ?")
                            await setupMessage.edit(embed=setup)
                            
                            def check(m):
                                return m.author == ctx.message.author and m.channel == ctx.channel
                            
                            battleName = await self.client.wait_for('message', timeout=60.0, check=check)
                            if(battleName.content != 'cancel'):
                                battleName = str(battleName.content)
                            else:
                                return await ctx.send("Commande annulée", delete_after=5.0)
                        else:
                            return await ctx.send("Ce channel n'existe pas!")
                    else:
                        return await ctx.send("Commande annulée", delete_after=5.0)
                except asyncio.TimeoutError:
                    return await ctx.send("Tu n'as pas répondu assez vite !", delete_after=5.0)
                else:
                    battle = discord.Embed(colour=discord.Colour.lighter_gray())
                    battle.set_thumbnail(url=ctx.guild.icon_url)
                    battle.set_author(name=f"{battleName}")
                    battle.add_field(name="<:HEAL:665640048225681448> **0 HEALERS** <:HEAL:665640048225681448>", value="\u200b")
                    battle.add_field(name="<:DPS:665640019725254676> **0 DPS** <:DPS:665640019725254676>", value="\u200b")
                    battle.add_field(name="<:TANK:665639984266739752> **0 TANK** <:TANK:665639984266739752>", value="\u200b") # \u200b
                    battle.set_footer(text="Total de 0 joueurs.")
                    battleMessage = await repChannel.send(embed=battle)

                    data[str(ctx.guild.id)]['rm'][str(battleMessage.id)] = {
                        "type": 3,
                        "<:HEAL:665640048225681448>": [0, "<:HEAL:665640048225681448> **{num} HEALERS** <:HEAL:665640048225681448>"],
                        "<:DPS:665640019725254676>": [1, "<:DPS:665640019725254676> **{num} DPS** <:DPS:665640019725254676>"],
                        "<:TANK:665639984266739752>": [2, "<:TANK:665639984266739752> **{num} TANK** <:TANK:665639984266739752>"]
                        }
                    
                    with open('infos.json', 'w') as f:
                        json.dump(data, f, indent=4)

                    await battleMessage.add_reaction('<:HEAL:665640048225681448>')
                    await battleMessage.add_reaction('<:DPS:665640019725254676>')
                    await battleMessage.add_reaction('<:TANK:665639984266739752>')
                    
                    logging.warning(f'new battle in {ctx.guild.name}')
                    setup.set_author(name="Envoyé !")
                    await setupMessage.edit(embed=setup)
                    await setupMessage.delete(delay=10.0)
##########################################################################################

################################ ON_RAW_REACTION_ADD ################################
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reactChannel = self.client.get_channel(payload.channel_id)
        if(str(reactChannel.type) == 'text'):
            if(payload.member.bot == False):
                guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
                with open('infos.json', 'r') as f:
                    data = json.load(f)
                try:
                    rmType = data[str(guild.id)]['rm'][str(payload.message_id)]["type"]
######################### rM role
                    if(rmType == 0):
                        try:
                            role = guild.get_role(data[str(guild.id)]['rm'][str(payload.message_id)][str(payload.emoji)])
                        except:
                            logging.warning('error get_role add')
                        if(role is not None):
                            await payload.member.add_roles(role)
                            logging.warning(f'rM role add in {guild.name}')
                        else:
                            logging.warning('error role add')
######################### rM list
                    elif(rmType == 1):
                        rmList = data[str(guild.id)]['rm'][str(payload.message_id)]
                        message = await reactChannel.fetch_message(payload.message_id)
                        
                        rmListEmbed = message.embeds[0]
                        if(str(payload.emoji) in rmList):
                            index = rmList[str(payload.emoji)][0]
                            listValue = rmListEmbed.fields[index].value
                            try:
                                listName = rmList[str(payload.emoji)][1]
                                if("{num}" in listName):
                                    num = message.reactions[index].count - 1
                                    newListName = str(eval(f'f"""{listName}"""'))
                                else:
                                    newListName = listName
                            except NameError:
                                newListName = 'ARGUMENT ERROR'
                            finally:
                                rmListEmbed.set_field_at(index=index, name=newListName, value=listValue + "\n" + str(payload.member.name))

                                total = -len(message.reactions)
                                for index, reaction in enumerate(message.reactions):
                                    total = total + message.reactions[index].count
                                rmListEmbed.set_footer(text=f"Total de {total} participations.")

                                await message.edit(embed=rmListEmbed)
                                logging.warning(f'rM category update in {guild.name}')
######################### COUNTER
                    elif(rmType == 2 and str(payload.emoji) == '⬆️' or rmType == 2 and str(payload.emoji) == '⬇️'):
                        message = await reactChannel.fetch_message(payload.message_id)
                        rmEmbed = message.embeds[0]
                        number = data[str(guild.id)]['rm'][str(payload.message_id)]['number']

                        if(str(payload.emoji) == '⬆️'):
                            number = number + 1
                        elif(str(payload.emoji) == '⬇️'):
                            number = number - 1
                        
                        data[str(guild.id)]['rm'][str(payload.message_id)]['number'] = number  
                        with open('infos.json', 'w') as f:
                            json.dump(data, f, indent=4)
                        
                        await message.remove_reaction(payload.emoji, payload.member)
                        
                        rmEmbed.set_field_at(index=0, name=str(number), value="\u200b")
                        await message.edit(embed=rmEmbed)
                        
                        logging.warning(f'rM counter update in {guild.name}')
######################### BATTLE
                    elif(rmType == 3):
                        message = await reactChannel.fetch_message(payload.message_id)
                        rmListEmbed = message.embeds[0]
                        for index in range(3):
                            listValue = rmListEmbed.fields[index].value
                            if(payload.member.name in listValue):
                                await payload.member.send('Tu as deja réagi a une autre classe !')
                                return await message.remove_reaction(payload.emoji, payload.member)
                            
                        rmList = data[str(guild.id)]['rm'][str(payload.message_id)]
                        if(str(payload.emoji) in rmList):
                            index = rmList[str(payload.emoji)][0]
                            listValue = rmListEmbed.fields[index].value
                            try:
                                listName = rmList[str(payload.emoji)][1]
                                if("{num}" in listName):
                                    num = message.reactions[index].count - 1
                                    newListName = str(eval(f'f"""{listName}"""'))
                                else:
                                    newListName = listName
                            except NameError:
                                newListName = 'ARGUMENT ERROR'
                            finally:
                                rmListEmbed.set_field_at(index=index, name=newListName, value=listValue + "\n" + str(payload.member.name))

                                total = -len(message.reactions)
                                for index, reaction in enumerate(message.reactions):
                                    total = total + message.reactions[index].count
                                rmListEmbed.set_footer(text=f"Total de {total} participations.")

                                await message.edit(embed=rmListEmbed)
                                logging.warning(f'battle update in {guild.name}')
                except KeyError:
                    return
#############################################################################################

################################ ON_RAW_REACTION_REMOVE ################################
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reactChannel = self.client.get_channel(payload.channel_id)
        if(str(reactChannel.type) == 'text'):
            guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
            user = await guild.fetch_member(payload.user_id)
            with open('infos.json', 'r') as f:
                data = json.load(f)
            try:
                rmType = data[str(guild.id)]['rm'][str(payload.message_id)]["type"]
            except KeyError:
                return logging.warning('rmType KeyError')
######################### rM role
            if(rmType == 0):
                try:
                    role = guild.get_role(data[str(guild.id)]['rm'][str(payload.message_id)][str(payload.emoji)])
                except:
                    logging.warning('error get_role add')
                if(role is not None):
                    await user.remove_roles(role)
                    logging.warning(f'rM role remove in {guild.name}')
                else:
                    logging.warning('error role remove')
######################### rM category
            elif(rmType == 1):
                rmList = data[str(guild.id)]['rm'][str(payload.message_id)]
                message = await reactChannel.fetch_message(payload.message_id)
                
                rmListEmbed = message.embeds[0]
                if(str(payload.emoji) in rmList):
                    index = rmList[str(payload.emoji)][0]
                    listValue = rmListEmbed.fields[index].value
                    try:
                        listName = rmList[str(payload.emoji)][1]
                        if("{num}" in listName):
                            num = message.reactions[index].count - 1
                            newListName = str(eval(f'f"""{listName}"""'))
                        else:
                            newListName = listName
                    except NameError:
                        newListName = 'ARGUMENT ERROR'
                    finally:
                        listValue = listValue.replace(user.name, '')
                        rmListEmbed.set_field_at(index=index, name=newListName, value=listValue)

                        total = -len(message.reactions)
                        for index, reaction in enumerate(message.reactions):
                            total = total + message.reactions[index].count
                        rmListEmbed.set_footer(text=f"Total de {total} participations.")

                        await message.edit(embed=rmListEmbed)
                        logging.warning(f'rM category update in {guild.name}')
            elif(rmType == 3):
######################### BATTLE
                rmList = data[str(guild.id)]['rm'][str(payload.message_id)]
                message = await reactChannel.fetch_message(payload.message_id)
                
                rmListEmbed = message.embeds[0]
                if(str(payload.emoji) in rmList):
                    index = rmList[str(payload.emoji)][0]
                    listValue = rmListEmbed.fields[index].value
                    try:
                        listName = rmList[str(payload.emoji)][1]
                        if("{num}" in listName):
                            num = message.reactions[index].count - 1
                            newListName = str(eval(f'f"""{listName}"""'))
                        else:
                            newListName = listName
                    except NameError:
                        newListName = 'ARGUMENT ERROR'
                    finally:
                        listValue = listValue.replace(user.name, '')
                        rmListEmbed.set_field_at(index=index, name=newListName, value=listValue)

                        total = -len(message.reactions)
                        for index, reaction in enumerate(message.reactions):
                            total = total + message.reactions[index].count
                        rmListEmbed.set_footer(text=f"Total de {total} participations.")

                        await message.edit(embed=rmListEmbed)
                        logging.warning(f'battle update in {guild.name}')
#############################################################################################

def setup(client):
    client.add_cog(rMessage(client))