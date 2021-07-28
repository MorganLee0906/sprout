import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import datetime
import os

def get_data(type, IATA, num, date):
    if type == 'passenger':
        res = requests.get('https://www.taoyuan-airport.com/uploads/flightx/a_flight_v4.txt')
        if res.content == '':
            return "source error"
        flist = res.content.decode('big5').split('\n')
        for i in range(len(flist)-1):
            print(flist[i])
            info = flist[i].split(',')
            if info != '':
                if date == info[8] and IATA == info[2] and (str(num) == str(info[4]) or str(' '+num) == str(info[4])):
                    return info
        return 404
    elif type == 'cargo':
        res = requests.get('https://www.taoyuan-airport.com/uploads/flightx/af_flight_v4.txt')
        if res.content == '':
            return "source error"
        flist = res.content.decode('big5').split('\n')
        for i in range(len(flist)-1):
            print(flist[i])
            info = flist[i].split(',')
            if info != '':
                if date == info[8] and IATA == info[2] and (str(num) == str(info[4]) or str(' '+num) == str(info[4])):
                    return info
        return 404
    else:
        return 'Type error!'
class flight_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    datetime_dt = datetime.datetime.today()
    @commands.command(
        help = '''
            取得桃園機場即時航班資訊，可查詢昨日到明日的航班。
            使用 '$flight passenger <航空公司代碼> <航班號> <日期>'    取得客機資訊
            使用 '$flight cargo <航空公司代碼> <航班號> <日期>'        取得貨機資訊
            日期格式:<yyyy/mm/dd>   (若無輸入日期則預設為今日)
            範例:'$flight passenger CI 159 2021/07/03' ->搜尋CI159(客機)於2021/07/03的航班資訊
            *僅能搜尋前一天到明日的航班*
            (本航班資訊為桃園機場公司提供，資料來源可能會有問題，導致無法正確輸出。)
         ''',
        brief = "Get Taoyuan Airport flight information"
    )
    async def flight(self, ctx, type, IATA, num, date = datetime_dt.strftime("%Y/%m/%d")):
        await ctx.send('Getting flight information...')
        res = get_data(type.lower(), IATA, num, date)
        if res == 404:
            await ctx.send('Not found.')
        elif res == "Type error!":
            await ctx.send('Type error!')
        elif res == "source error":
            await ctx.send('Source error!Please try again...')
        else:
            embed = discord.Embed(color = 0xffff37)
            if res[1] == 'A':
                res[1] = 'Arrival'
                #embed = discord.Embed(color = 0xffff37)
                embed.set_thumbnail(url = 'https://www.taoyuan-airport.com/assets/images/fast_tab_icon2.png')
            else:
                res[1] = 'Depature'
                embed = discord.Embed(color = 0x00ffff)
                embed.set_thumbnail(url = 'https://www.taoyuan-airport.com/assets/images/fast_tab_icon1.png')
            embed.add_field(name = 'Flight Number:',\
    	        value = str(res[2]+' '+res[4]),\
    	        inline = False)
            embed.add_field(name = 'Airline:',\
        	    value = str(res[3]+'('+res[2]+')'),\
        	    inline = False)
            embed.add_field(name = 'Destination:',\
        	    value = str(res[12]+' '+res[11]+'('+res[10]+')'),\
        	    inline = False)
            embed.add_field(name = 'Depature/Arrival:',\
    	        value = str(res[1]),\
    	        inline = False)
            embed.add_field(name = 'Estimated date:',\
    	        value = str(res[8]),\
    	        inline = False)
            embed.add_field(name = 'Estimated time:',\
    	        value = str(res[9]),\
    	        inline = False)
            embed.add_field(name = 'Terminal:', 
    	        value = str(res[0]),\
    	        inline = False)
            if res[13] != '取消CANCELLED          ':
                embed.add_field(name = 'Gate:', 
    	            value = str(res[5]),\
    	            inline = False)
            if type.lower() == 'passenger':
                if res[1] == 'Arrival' and res[13] != '取消CANCELLED          ':
                    embed.add_field(name = 'Baggage carousel:', 
    	            value = str(res[18]),\
    	            inline = False)
                if res[1] == 'Depature' and res[13] != '取消CANCELLED          ':
                    embed.add_field(name = 'Check-in counter:', 
    	            value = str(res[19]),\
    	            inline = False)
            embed.add_field(name = 'Status:', 
    	        value = str(res[13]),\
    	        inline = False)
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(flight_info(bot))
    