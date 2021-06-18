import discord
from discord.ext import commands
import random
import json
import requests
import os

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def de(ctx, n=1):
    await ctx.channel.purge(limit = n+1)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))

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
async def meme(ctx):
    response = requests.get("https://some-random-api.ml/meme")
    json_data = json.loads(response.text)
    url = json_data['image']
    await ctx.send(url)

animals = ['cat', 'dog', 'panda', 'red_panda', 'fox', 'birb', 'koala']
@bot.command()
async def ani(ctx):
    animal = random.choice(animals)
    url = 'https://some-random-api.ml/img/' + animal
    response = requests.get(url)
    json_data = json.loads(response.text)
    url = json_data['link']
    await ctx.send(url)

@bot.command()
async def im(ctx):
    name = str(random.randint(0,5)) + '.png'
    await ctx.send(file=discord.File(name))

@bot.command()
async def img(ctx):
    url = 'https://picsum.photos/id/' + str(random.randint(0,1000)) + '/1500/1000'
    await ctx.send(url)

@bot.command()
async def m(ctx):
    score = 0
    while(1):
        num2 = random.randint(11,99)
        num1 = random.randint(11,99)
        await ctx.send(str(num1) + ' + ' + str(num2) + ' = ?')
        try:
            msg = await bot.wait_for('message',timeout=10)
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

bot.run(os.getenv('token'))