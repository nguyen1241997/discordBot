import discord
from discord.ext import commands
import random
import os
import requests
import json
import time
import datetime 

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def he(ctx):
    a = "```.ping```"
    b = "```.de <number>```"
    c = "```.choose <a> <b>```"
    d = "```.img```"
    e = "```.m```"
    await ctx.send(a)
    await ctx.send(b)
    await ctx.send(c)
    await ctx.send(d)
    await ctx.send(e)

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} ms')

@bot.command()
async def de(ctx, n=1):
    await ctx.channel.purge(limit = n+1)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return quote

@bot.command()
async def quote(ctx):
    quote = get_quote()
    await ctx.send(quote)

@bot.command()
async def img(ctx):
    url = 'https://picsum.photos/id/' + str(random.randint(0,1000)) + '/1500/1000'
    await ctx.send(url)

@bot.command()
async def m(ctx):
    score = 0
    await ctx.send('You have 6s to answer. Good luck!')
    time.sleep(3)
    while(1):
        num2 = random.randint(11,99)
        num1 = random.randint(11,99)
        await ctx.send(str(num1) + ' + ' + str(num2) + ' = ?')
        try:
            msg = await bot.wait_for('message',timeout=5)
        except:
            break
        if msg.author == bot.user:
            msg = await bot.wait_for('message')
        try:
            ans = int(msg.content)
        except:
            break
        if ans == num1 + num2 :
            await ctx.send('Correct.')
            score += 10
        else:
            await ctx.send('Incorrect.')
            break
    await ctx.send('Game stoped.')
    await ctx.send(f'Congratulation! You got {score} points.')

    
@bot.command()
async def wea(ctx, city):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=6013623378bf73ee1f63a2a3c08b8739"
    response = requests.get(url)
    json_data = json.loads(response.text)
    
    coordinate =  json_data['coord']
    weather = json_data['weather'][0]
    main = json_data['main']
    time = json_data['timezone']
    
    await ctx.send("***Coordinate:***")
    for x in coordinate:
        await ctx.send('- ' + x + ': ' + str(coordinate[x]))
    await ctx.send("***Weather:***")
    
    for x in weather:
        if x=='id' or x=='icon': continue
        await ctx.send('- ' + x + ': ' + str(weather[x]))
        
    for x in main:
        if x=='pressure' or x=='grnd_level' or x=='sea_level': continue
        if x=='humidity':
            await ctx.send('- ' + x + ': ' + str(main[x]))
        else:
            await ctx.send('- ' + x + ': ' + str(round((main[x]-273.15),1)))
            
    tz = datetime.timezone(datetime.timedelta(seconds=int(time)))
    timezone = datetime.datetime.now(tz = tz).strftime("%H:%M:%S - %m/%d/%Y")
    await ctx.send("***Time and Date: ***")
    await ctx.send(timezone)

    
@bot.command()
async def covid(ctx, * , country):
    url = "https://api.covid19api.com/summary"
    response = requests.get(url)
    json_data = json.loads(response.text)
    
    world = json_data['Global']
    countries = json_data['Countries']
    
    await ctx.send("***Global:***")
    for x in world:
        if x=='NewRecovered' or x=='TotalRecovered': continue
        await ctx.send('- ' + x + ': ' + str(world[x]))
        
    for x in countries:
        if x['Country']==country:
            await ctx.send('***' + country +':***')
            for y in x:
                if y=='ID' or y=='Country' or y=='CountryCode' or y=='Slug' or y=='NewRecovered' or y=='TotalRecovered' or y=='Premium': continue
                await ctx.send('- ' + y + ': ' + str(x[y]))
            break
    
    
bot.run(os.getenv('token'))
