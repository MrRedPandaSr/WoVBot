import os
import discord
from discord.ext import commands
from datetime import datetime
from events import Events
import asyncio
from users import Users

class GuildEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = Events('events.dat')
        self.users = Users('users.dat')
        bot.loop.create_task(self.auto_load())
    
    
    async def auto_load(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            self.events.load_events()
            await asyncio.sleep(60)
    
    #Admin/Gm/Lootmaster commands------------------

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def newEvent(self, ctx, name:str, start:str, end:str, max:int, desc:str):
        '''
        Creates a new event spanning the given duration.
        Syntax is: !newEvent "Event Name" "Start Date/Time" "End Date/Time" "max number of people" "event description"
        Date/Time syntax should be as follows: 'Aug 26 2019  11:00PM'
        '''
        start_date = str(datetime.strptime(start, '%b %d %Y %I:%M%p'))
        end_date = str(datetime.strptime(end, '%b %d %Y %I:%M%p'))


        player = self.users.find_user(ctx.author.id).wow_name
        print(player)
        if player is not False:
            new_event = self.events.add_event(name,start_date,end_date,max,desc)
            #self.events.join_event(new_event,player)

        #Return command to join the newly created event.
        await ctx.send('A new event has been created, join it by typing !joinEvent '+str(new_event))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def cancelEvent(self, ctx, event_id:int):
        event = self.events.find_event(event_id)
        if event is not False:
            #Should probably check user here to make sure they exist before adding to event.
            event.cancel_event()
            await ctx.send('The event has been cancelled.')
        else:
            await ctx.send('The event was not found')
  
#End of admin only commands:----------------

    @commands.command()
    async def showEvent(self, ctx, event_id:int):
        '''
        Shows details of the event from the given event ID
        '''
        event = self.events.find_event(event_id)
        if event is not False:
            out = "```\n"
            out += str('Event Name: '+event.name+'\n'+'Starting in: '+str(event.starting_in())+'\n'+'Slots: '+str(len(event.players))+'/'+str(event.max)+'\n'+'Description: '+event.description+'\n')
            out += 'Players:\n'
            for player in event.get_players:
                out += '-'+player+'\n```'
            await ctx.send(out)
        else:
            await ctx.send('Event was not found!')
        

    @commands.command()
    async def showEvents(self, ctx):
        '''
        Shows details of all currently active events.
        '''
        #Could format this to be an embed or a raid calendar.
        out = "```\n"
        out += str('ID\tEvent Name\tPlayers\tStarting\n')
        for event in self.events.events:
            if event.status in range(0,1): # Selects events that haven't been completed or cancelled.
                out += str(str(event.id) + '\t' + event.event_name +'\t'+ str(len(event.players)) + '/' + str(event.max)+'\t'+event.starting_in()+'\n')
        out += "```"
        await ctx.send(out)
    
    @commands.command()
    async def joinEvent(self, ctx, event_id:int):
        '''
        Joins the event from the given event ID.  Note this will only work if the player has !setmain'd
        '''
        event = self.events.find_event(event_id)
        player = self.users.find_user(ctx.author.id)
        if event is not False and player is not False:
            player = player.wow_name
            self.events.join_event(event_id,player)
            out = 'You have joined the event: '+str(event.event_name)+'\n'
            out += str('```ID\tEvent Name\tPlayers\tStarting\n')
            out += str(str(event.id) + '\t' + event.event_name +'\t'+ str(len(event.players)) + '/' + str(event.max)+'\t'+str(event.start_date)+'\n```')
            await ctx.send(out)

    @commands.command()
    async def leaveEvent(self, ctx, event_id:int):
        '''
        Removes the player from the given event if the player has joined the event.
        '''
        event = self.events.find_event(event_id)
        player = self.users.find_user(ctx.author.id)
        if event is not False and player is not False:
            #Should probably check user here to make sure they exist before adding to event.
            player = player.wow_name
            self.events.leave_event(event_id,player)
            await ctx.send('You have left the event: '+str(event.event_name))


def setup(bot):
    bot.add_cog(GuildEvents(bot))