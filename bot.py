import os
import discord
from discord.ext import commands
import json
import asyncio
import inspect

prefix = "!"

bot = commands.Bot(command_prefix=prefix)
TOKEN = 'YOUR BOT TOKEN'

#Set bot to playing !command | WoW Classic.
bot.activity=discord.Game('!command | WoWClassic')

#Init cogs from filepath
path = 'cogs.'
extensions = [x.replace('.py', '') for x in os.listdir(path) if x.endswith('.py')]


def load_extension(cog, path='cogs.'):
    '''Loads a given cog to the bot'''
    members = inspect.getmembers(cog)
    for name, member in members:
        if name.startswith('on_'):
            bot.add_listener(member, name)
    try:
        bot.load_extension(f'{path}{cog}')
    except Exception as e:
        print(f'LoadError: {cog}\n{type(e).__name__}: {e}')


def load_extensions(cogs, path='cogs.'):
    '''Loads all cogs to the bot'''
    for cog in cogs:
        members = inspect.getmembers(cog)
        for name, member in members:
            if name.startswith('on_'):
                bot.add_listener(member, name)
        try:
            bot.load_extension(f'{path}{cog}')
        except Exception as e:
            print(f'LoadError: {cog}\n{type(e).__name__}: {e}')

#Load cogs
load_extensions(extensions)


@bot.event
async def on_ready():
    print('Bot is online and ready to go.')

@bot.event
async def on_message(message):
    print(str(message.author) + ": " + str(message.content))
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    '''
    Triggers when a member joins the discord
    '''
    
    await member.send("```\nWelcome to the World of Vanilla Server!\nThe first thing you should do is set your WoW Character name by typing !setmain <Charname> in any channel.\n You can then view your DKP with !dkp or transfer it with !transfer <User> <Amount>. \n For more help and info, just type !help. \n```")


##ADMIN ONLY COMMANDS------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount):
        messages.append(message)
    try:
        await channel.delete_messages(messages)
    except:
        for message in messages:
            await channel.purge(limit=amount,oldest_first=True,bulk=True)


@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user:discord.User):
    try:
        guild = ctx.guild
        await guild.kick(user)
        await ctx.send(str(user)+ ' booted.')
    except:
        await ctx.send('User could not be kicked.')
##END OF ADMIN ONLY COMMANDS-----------------------

#WoVBot general commands:-----------

@bot.command()
async def ping(ctx):
    '''
    Returns the current ping of WoVBot.
    '''

    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send('<@'+str(ctx.author.id)+'> My ping is: '+str(float(latency).__format__('3.2f'))+'ms')


#end of WoVBot General Commands:----------------
                
#Finally, start the bot.
bot.run(TOKEN)