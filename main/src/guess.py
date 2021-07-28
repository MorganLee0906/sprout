# 檔名：guess.py
# 功能：猜數字

#################################################################
# TODO: 實作猜數字
# 分類: 作業 (10 pts)
# HINT: 認真上課
#################################################################
from typing import AnyStr
import discord
from discord.ext import commands
import random

class Guess(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    @commands.command(help = '''
    Guess a 4-digit number that doesn't contain 0.
    Press q or enter 'quit' to stop game.
    ''', brief = "Guess number!.")
    async def guess(self,ctx):
        def is_valid(m):
            return m.author == ctx.author
        await ctx.send("Guess a 4-digit number that doesn't contain 0.")
        ans =""
        for _ in range(4):
            ans+=str(random.randint(1,9))
        print(ans)
        
        for _ in range(30):
            g = await self.bot.wait_for('message', check = is_valid, timeout = 300.0)
            guess = g.content.strip()
            print(guess)
            if guess.lower() == 'quit':
                await ctx.send("Stop guess.")
                return
            for i in range(4):
                if guess[i].isdigit() == False:
                    await ctx.send("illegal input! please try again.")

            a = sum([1 for i in range(4) if guess[i] == ans[i]])
            b = sum([1 for i in range(4) if guess[i] in ans])-a
            if guess == ans:
                await ctx.send('Correct!')
                return
            else:
                await ctx.send(f"{a}A{b}B")
        await ctx.send('Guess too many times!')

def setup(bot):
    bot.add_cog(Guess(bot))
