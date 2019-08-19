from open_search import OpenSearch, OpenSearchError, SearchObjectError
import discord
import os
from discord.ext import commands

class Classicdb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def classicdb(self,ctx,db:str,*item:str):
        '''
        Queries the selected database for an item or spell.
            Arguments: 
                db: Can be item or spell
                item: item or spell name
        '''
        search = str(item)
        channel = ctx.channel
        #Delete query message
        # msgs = []
        # msgs.append(ctx.message)
        # await channel.delete_messages(msgs)
        #---
        try:
            oser = OpenSearch(db, search)
            oser.search_results.get_tooltip_data()
            image = oser.search_results.image
            await channel.send(file=discord.File(image))
            os.remove(image)
        except (OpenSearchError, SearchObjectError) as e:
            await channel.send(e)

def setup(bot):
    bot.add_cog(Classicdb(bot))