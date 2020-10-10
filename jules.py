import os
import json
import time
import discord
import subprocess
import requests
from discord.ext import commands
from helium_analysis_tools.classes import Hotspots
from helium_analysis_tools import utils
import genkml

#from dotenv import load_dotenv
#load_dotenv()
#DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_TOKEN = 'put your bot token here'
bot=commands.Bot(command_prefix='$')
h=Hotspots.Hotspots()


@bot.command(name='api',
             help="",
             brief="{hotspot_name} witness")
async def api(ctx,hotspot,command):
    try:
        addr=h.hspot_by_name[hotspot]['address']
        if command=='witness':
            url='https://api.helium.io/v1/hotspots/'+addr+'/witnesses'
            await ctx.channel.send("`"+url+"`")
            page=requests.get(url=url).json()
            page=page['data']
            print(page)
            for witness in page:
                await ctx.channel.send("`"+json.dumps(witness,indent=1)+"`")
    except Exception as e:
        print(e)

@bot.command(name='polar',
             help="Calculated FSPL is divided by average RSSI and plotted on polar coordinate.",
             brief="{hotspot_name}")
async def polar(ctx, hotspot):
    #try:
    addr=h.hspot_by_name[hotspot]['address']
    cmd='python helium_analysis_tools\\analyze_hotspot.py -x poc_polar -n '+str(hotspot)
    a=subprocess.Popen(cmd)
    a.communicate()
    await ctx.channel.send(file=discord.File(hotspot+'_map.html'))
    #except Exception as e:
    #    print(e)


@bot.command(name='kml',
             help="",
             brief="returns the latest kml file for google earth containing all hotspots")
async def kml(ctx):
    try:
        if not os.path.exists('hotspots.kml'):
            genkml.genkml()
        file_time = os.path.getmtime('hotspots.kml') 
        if (time.time() - file_time) / 3600 > 1:
            await ctx.channel.send('Generating new file...')
            os.remove('hotspots.kml')
            genkml.genkml()
        await ctx.channel.send(file=discord.File('hotspots.kml'))
    except Exception as e:
        print(e)


@bot.command(name='hat',
             help="refer to https://github.com/Carniverous19/helium_analysis_tools",
             brief="{hotspot_name} or para1 command as normal $hat -x poc_summary --address {hotspot address}")
async def hat(ctx, *args):
    try:
        response = ''
        for arg in args:
            response = response+' '+arg
        
        
        if len(args)==1:
            cmd="python helium_analysis_tools\\analyze_hotspot.py -x poc_v10 -n " + args[0] #--address '+str(addr)
            #try:
            await ctx.channel.send('`'+cmd+'`')
            a=subprocess.Popen(cmd,stdout=subprocess.PIPE)#,stderr=subprocess.STDOUT)
            out=a.communicate()
            await ctx.channel.send("`"+str(out[0], 'utf-8')+"`")
            #except ValueError:
                
            #await ctx.channel.send("That's not a hotspot. Use dashes like yellow-rubber-ducky")
            #    return

            
            cmd="python helium_analysis_tools\\analyze_hotspot.py -x poc_reliability -n " + args[0]#--address '+str(addr)
            await ctx.channel.send('`'+cmd+'`')
            a=subprocess.Popen(cmd,stdout=subprocess.PIPE)#,stderr=subprocess.STDOUT)
            out=a.communicate()
            await ctx.channel.send("`"+str(out[0], 'utf-8')+"`")

        else:
            cmd="python helium_analysis_tools\\analyze_hotspot.py " + response
            await ctx.channel.send('`'+cmd+'`')
            a=subprocess.Popen(cmd,stdout=subprocess.PIPE)#,stderr=subprocess.STDOUT)
            out=a.communicate()

            await ctx.channel.send("`"+str(out[0], 'utf-8')+"`")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("hello")

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
