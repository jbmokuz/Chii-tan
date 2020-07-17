import discord, os
from discord.ext import commands
from functions import *
import requests, sys, re
import xml.etree.ElementTree as ET
import copy
import urllib


TOKEN = os.environ["DISCORD_TT_TOKEN"]
ROOM_KEY = os.environ["TENHOU_TT_KEY"]

bot = commands.Bot("!")
gi = GameInstance()

def getVars(ctx):
    player = ctx.author
    chan = ctx.channel
    return player,chan


@bot.command()
async def start(ctx, p1=None, p2=None, p3=None, p4=None, randomSeat="true"):
    """
    Start Tenhou Game
    Args:
        player1 player2 player3 player4 randomSeating=[true/false]
    """
    
    player, chan = getVars(ctx)

    if (p1 == None or p2 == None or p3 == None or p4 == None):
        await chan.send(f"Please specify 4 players space separated")
        return

    player_names = [p1,p2,p3,p4]

    data = {
        "L":ROOM_KEY,
        "R2":gi.rules,
        "RND":"default",
        "WG":"1"
        }
    
    if randomSeat.lower() != "false" and randomSeat.lower() != "no":
        random.shuffle(player_names)
        
    data["M"] = "\r\n".join(player_names)

    resp = requests.post('https://tenhou.net/cs/edit/start.cgi',data=data)
    if resp.status_code != 200:
        await chan.send(f"http error {resp.status_code} :<")
        return
    await chan.send(urllib.parse.unquote("&".join(resp.url.split("&")[1:])))

@bot.command()
async def start_at(ctx, p1=None, p2=None, p3=None, p4=None, randomSeat="true"):
    """
    Start Tenhou Game
    Args:
        player1 player2 player3 player4 randomSeating=[true/false]
    """
    
    player, chan = getVars(ctx)

    if (p1 == None or p2 == None or p3 == None or p4 == None):
        await chan.send(f"Please specify 4 players space separated")
        return

    player_names = [p1,p2,p3,p4]
    player_parsed = []
    
    for player in player_names:
        for i in chan.guild.members:
            if str(i.id) in player:
                name = i.display_name
                try:
                    player_parsed.append(re.search("\((.*)/.*\)",name).group(1))
                except:
                    pass

    await chan.send("Players "+",".join(player_parsed))
    
    data = {
        "L":ROOM_KEY,
        "R2":gi.rules,
        "RND":"default",
        "WG":"1"
        }
    
    if randomSeat.lower() != "false" and randomSeat.lower() != "no":
        random.shuffle(player_parsed)
        
    data["M"] = "\r\n".join(player_parsed)

    resp = requests.post('https://tenhou.net/cs/edit/start.cgi',data=data)
    if resp.status_code != 200:
        await chan.send(f"http error {resp.status_code} :<")
        return
    await chan.send(urllib.parse.unquote("&".join(resp.url.split("&")[1:])))


@bot.command(aliases=['p'])
async def ping(ctx):
    """
    Ping!
    """

    player, chan = getVars(ctx)
    
    player = ctx.author
    chan = ctx.channel
    await chan.send("Chii?")

@bot.command()
async def score(ctx, log=None):
    """
    Add 1.5 to the scores in a Tenhou log
    Args:
        log:
            A full url or just the log id
    """
    player, chan = getVars(ctx)
    
    player = ctx.author
    chan = ctx.channel

    if log == None:
        await chan.send("usage: !score [tenhou_log]\n Example: !score https://tenhou.net/0/?log=2020051313gm-0209-19713-10df4ad2&tw=1")
        
    ret = gi.parseGame(log)
    if ret != 0:
        await chan.send(gi.lastError)
        return
    
    ret = "Chii!```Raw   Adjust Name\n"
    for player,raw,adjust in gi.lastError:
        if raw >= 0:
            ret += f" {raw}  {format(adjust,'.2f')} {player}\n"
        else:
            ret += f"{raw} {format(adjust,'.2f')} {player}\n"
    ret += "```"
    
    await chan.send(ret)
    
@bot.event
async def on_ready():
    print("Time to TwinTail!")
    print("Logged in as: {}".format(bot.user.name))

@bot.event
async def on_error(event, *args, **kwargs):
    print("ERROR!")
    print("Error from:", event)
    print("Error context:", args, kwargs)

    from sys import exc_info

    exc_type, value, traceback = exc_info()
    print("Exception type:", exc_type)
    print("Exception value:", value)
    print("Exception traceback object:", traceback)

    
bot.run(TOKEN)
