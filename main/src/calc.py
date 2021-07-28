import discord
from discord.ext import commands
from math import *
def calculator(s):
    s = s.replace('^','**')
    s = s.replace('log','log10')
    s = s.replace('ln','log')
    #print(s)
    i, t = len(s)-1, 0
    while i>0:
        if s[i] == '!':
            if s[i-1].isdigit():
                t = i
                i -= 1
                while s[i].isdigit():
                    i-=1
                fnum = s[i+1:t]
                s = s[0:i+1] + 'factorial(' + fnum + ')' + s[t+1:len(s)-1]
            else:
                t = i
                r = 1
                i -= 2
                while r:
                    if s[i] == ')':
                        r += 1
                    if s[i] == '(':
                        r -= 1
                    i-=1
                num = s[i+1:t]
                s = s[0:i+1] + 'factorital(' + num + ')' + s[t+1:len(s)-1]
        i-=1
    try:
        #print(s)
        ans = round(eval(s),5)
        return str(ans)
    except:
        ans = 'Error!'
        return ans

class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help = '''
            計算一行算式(僅支援+,-,*,/,^,log,ln運算)
         ''',
        brief = "Calculate a formula!"
    )
    async def calc(self, ctx, s):
        #print(s)
        ans = calculator(s)
        #print(ans)
        if ans != 'Error!':
            await ctx.send(s + ' = ' + ans)
        else:
            await ctx.send('Error!')
        
def setup(bot):
    bot.add_cog(Calc(bot))
            

