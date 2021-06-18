import discord
from discord.ext import commands
import random
import os

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)} ms')

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