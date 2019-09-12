import os
import discord
from discord.ext import commands
from users import Users
import asyncio

class Dkp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = Users('users.dat')
        bot.loop.create_task(self.auto_load())
    
    
    async def auto_load(self):
        await self.bot.wait_until_ready()
        while True:
            print('Updating users')
            self.users.users = self.users.load_users()
            await asyncio.sleep(60)
    
    #Admin/Gm/Lootmaster commands------------------

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def givedkp(self, ctx, user:str, amount:int):
        '''
        Gives <Amount> of DKP to user out of thin air.
        '''
        print(str(user))
        recipient = self.users.find_user(user)
        recipient.dkp += amount
        self.users.save_users()
        await ctx.send('<@'+str(ctx.author.id)+'> Awarded '+recipient.id+' '+str(amount)+' DKP!')



    @commands.command()
    @commands.has_permissions(administrator=True)
    async def takedkp(self, ctx, user:str, amount:int):
        '''
        Takes <Amount> of DKP from user.
        '''
        #THATS A FUCKING 50DKP MINUS!!
        print(str(user))
        recipient = self.users.find_user(user)
        if recipient.dkp >= amount:
            recipient.dkp -= amount
            await ctx.send('<@'+str(ctx.author.id)+'> Removed '+str(amount)+' DKP from '+recipient.id+'!')
        else:
            recipient.dkp = 0
            await ctx.send('<@'+str(ctx.author.id)+'> Rinsed all of '+recipient.id+'\'s DKP!')
        
        self.users.save_users()


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dkp_a(self,ctx):
        '''
        Returns entire guild's DKP balance.
        '''
        usersout = '```\n'
        for user in self.users.users:
            usersout += user.wow_name+'\'s DKP Balance: '+ str(user.dkp) +' DKP\n'
        usersout += '```'
        await ctx.send(usersout)
    
#End of admin only commands:----------------


    @commands.command()
    async def setmain(self, ctx, character:str):
        '''
        Allows you to set the character name of your WoW Classic main.
        Useage: !setmain <Charactername>
        '''
        
        usr_id = '<@'+str(ctx.author.id)+'>'
        usr_name = str(ctx.author)
        wow_name = character

        saving = True

        for user in self.users.users:   
            if user.id == usr_id:
                await ctx.send('<@'+str(ctx.author.id)+'> You\'ve already set your main!')
                saving = False
                #Already set main.
            elif user.wow_name == wow_name:
                await ctx.send('<@'+str(ctx.author.id)+'> Adding main failed, WoW name already associated to '+ user.name)
                saving = False
        if saving:
            self.users.add_user(usr_id,usr_name,wow_name)
            await ctx.send('<@'+str(ctx.author.id)+'> your main has been set to '+ character)
            role = discord.utils.get(ctx.author.guild.roles, name="Peon")
            #Assign peon role automatically.
            await ctx.author.add_roles(role)
    
      
    @commands.command()
    async def dkp(self,ctx):
        '''
        Prints your DKP balance.
        Usage: !dkp
        '''
        user = self.users.find_user(ctx.author.id)
        if user is not False:
            await ctx.send('```\n'+user.wow_name+'\'s DKP Balance:\n'+ str(user.dkp) +'\n```')
        else:
            print('Have you set your WoW Main character yet? Try !setmain <character>')

        # for user in self.users.users:
        #     if user.id == ('<@'+str(ctx.author.id)+'>'):
        #         await ctx.send('```\n'+user.wow_name+'\'s DKP Balance:\n'+ str(user.dkp) +'\n```')

    @commands.command()
    async def transferdkp(self, ctx, recipient:str, amount:int):
        '''
        Allows you to transfer DKP to another user.
        Recieving user must have !setmain\'ed, otherwise transaction will fail.
        Usage: !transferdkp @User <Amount>
        '''
        #Nicknames contain a !, if this is the case remove it.
        if(recipient[2] == '!'):
            # recipient = recipient[0:2] + recipient[3:]
            recipient.replace('!','')

        #Checks
        sender = self.users.find_user(ctx.author.id)
        if sender is not False:
            if sender.dkp >= amount:
                recip = self.users.find_user(recipient)
                if recip is not False:
                    #do transfer
                    recip.dkp += amount
                    sender.dkp -= amount
                    self.users.save_users()
                    await ctx.send(sender.id+' Successfully transferred '+str(amount)+' DKP to '+recipient)
                else:
                   await ctx.send(recipient+' Has not yet !setmained, so cannot recieve DKP.') 
            else:
                await ctx.send(sender.id+' You do not have enough DKP for this transaction.') 
        else:
            await ctx.send(sender.id+' You have not yet used !setmain to set your character name.  Do this to start transferring DKP.') 
        


def setup(bot):
    bot.add_cog(Dkp(bot))