import os
import discord
from discord.ext import commands
import datetime
from events import Events
import asyncio
from users import Users


class GuildEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = Events("events.dat")
        #Requires the DKP Cog!
        dkp = bot.get_cog("Dkp")
        self.users = dkp.users
        ##  
        bot.loop.create_task(self.auto_load())
    
    
    async def auto_load(self):
        await self.bot.wait_until_ready()
        while True:
            print('Updating events')
            self.events.events = self.events.load_events()
            await self.update_events()
            await asyncio.sleep(60)

    async def update_events(self):
        await self.bot.wait_until_ready()
        
        #dto of event start / end times
        for event in self.events.events:
            dto_s = datetime.datetime.strptime(str(event.start_date), '%Y-%m-%d %H:%M:%S')
            dto_f = datetime.datetime.strptime(str(event.end_date), '%Y-%m-%d %H:%M:%S')

            #EVENT STARTS IN 30 ISH MINUTES NOTIFICATION
            if event.status == 0:
                #If there is less than 30 minutes to event starting...
                if dto_s <= datetime.datetime.now() + datetime.timedelta(minutes=30) and datetime.datetime.now() < dto_f: 
                    event.ready_event()
                    if len(event.players) == event.max: 
                        ##Make new voice channel for event
                        channel = self.bot.get_channel(event.chan)
                        channel = channel.guild.categories[1]
                        nchannel = await channel.create_voice_channel(event.event_name,user_limit=event.max)
                        inviteLinq = await nchannel.create_invite(max_uses = event.max)
                        
                        #channel = self.bot.get_channel(event.chan)
                        #await channel.send("The event " + event.event_name + " is starting in "+event.starting_in()+"\n Get online and prepare to battle!")
                        for player in event.players:
                            user = self.users.find_user_w(player)
                            userid = int(str(user.id)[2:-1])
                            userO = self.bot.get_user(userid)
                            if userO != None:
                                await userO.send("The event " + event.event_name + " is starting in "+event.starting_in()+"\n Get online and prepare to battle!\nJoin the voice channel here: "+inviteLinq.url)
                        event.chan = nchannel.id
                        self.events.save_events()    
                    else:
                        #Not enough players to start event
                        event.cancel_event()
                        self.events.save_events()
                        return False         
                #WHEN EVENT START TIME IS MET
                if dto_s <= datetime.datetime.now() and event.status == 1:
                        event.start_event()
                        for player in event.players:
                                user = self.users.find_user_w(player)
                                userid = int(str(user.id)[2:-1])
                                userO = self.bot.get_user(userid)
                                if userO != None:
                                    await userO.send("The event " + event.event_name + " is starting NOW!")
                    
            #TIME AFTER EVENT END
            if dto_f <= datetime.datetime.now():
                if event.status == 1:
                    channel = self.bot.get_channel(event.chan)
                    
                    event.finish_event()
                    self.events.save_events()
                    if channel != None:
                        if channel.type == discord.ChannelType.voice:
                            print('Deleting channel...')
                            await channel.delete(reason="The event has ended.")
                            
                #Sets event to complete but does not trigger dkp changes
                    
            
    
    #Admin/Gm/Lootmaster commands------------------

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def newEvent(self, ctx, name:str, start:str, end:str, max:int, desc:str):
        '''
        Creates a new event spanning the given duration.
        Syntax is: !newEvent "Event Name" "Start Date/Time" "End Date/Time" "max number of people" "event description"
        Date/Time syntax should be as follows: 'Aug 26 2019  11:00PM'
        '''
        start_date = str(datetime.datetime.strptime(start, '%b %d %Y %I:%M%p'))
        end_date = str(datetime.datetime.strptime(end, '%b %d %Y %I:%M%p'))


        player = self.users.find_user(ctx.author.id).wow_name
        print(player)
        if player is not False:
            new_event = self.events.add_event(ctx,name,start_date,end_date,max,desc)
            #self.events.join_event(new_event,player)

        #Return command to join the newly created event.
        await ctx.send('A new event has been created, join it by typing ```!joinEvent '+str(new_event)+'```')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def completeEvent(self, ctx, event_id:int):
        dkp_reward = 50
        event = self.events.find_event(event_id)
        if event is not False:
            #Should probably check user here to make sure they exist before adding to event.
            event.finish_event()
            await ctx.send('The event has finished.  Attendance DKP will now be distributed...')
            out = ''
            for player in event.players:
                user = self.users.find_user_w(player)
                if user is not False:
                    user.dkp += dkp_reward
                    out += str(dkp_reward)+'DKP Awarded to '+player+' for attending '+event.event_name+'.\n'
                else:
                    out += 'User not found \n'
            self.users.save_users()
            self.events.save_events()
            await ctx.send(out)
        else:
            await ctx.send('The event was not found')
    
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
            out += str('Event Name: '+event.event_name+'\n'+'Starts: '+str(event.start_date)+'\n'+'Description: '+event.description+'\n')
            out += 'Players: '+str(len(event.players))+'/'+str(event.max)+'\n'
            for player in event.get_players():
                out += '[+] '+player+'\n'
            out += '```'
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
            if event.status in range(0,2): # Selects events that haven't been completed or cancelled.
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
            if len(event.players) < event.max:
                player = player.wow_name
                if self.events.join_event(event_id,player):
                    out = 'You have joined the event: '+str(event.event_name)+'\n'
                    out += str('```ID\tEvent Name\tPlayers\tStarting\n')
                    out += str(str(event.id) + '\t' + event.event_name +'\t'+ str(len(event.players)) + '/' + str(event.max)+'\t'+str(event.start_date)+'\n```')
                    await ctx.send(out)
                else:
                    await ctx.send('Something went wrong!  Join_event returned false.')
            else:
                await ctx.send('Event is full, you cannot join!')
        else:
            await ctx.send('Either event was not found or you have not !setmain\'d')

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