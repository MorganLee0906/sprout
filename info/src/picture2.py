import discord
from discord.ext import commands
import os
import requests
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
from skimage import io

class Picture(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help = "Sent a picture url to get information.", brief = "Get EXIF information.")
    async def info(self, ctx, pic_url):
        try:
            response = requests.get(pic_url)
        except IndexError:
            return await ctx.send('Image invalid!')
        file = open(os.path.join("..", "storage", "temp.jpg"), "wb")
        file.write(response.content)
        file.close()
        img = Image.open(os.path.join("..", "storage", "temp.jpg"))
        exif = img._getexif()
        if exif != None:
            embed = discord.Embed(color = 0x00ffff)
            embed.set_thumbnail(url = pic_url)
            #print(exif.items())
            for tag, val in exif.items():
                key = TAGS.get(tag, tag)
                if key != 'MakerNote':
                    embed.add_field(name = key,\
                    value = str(val),\
                    inline = False)
                    print(str(key)+':'+str(val))
            await ctx.send(embed = embed)
        else:
            await ctx.send("No exif information in this picture.")

    @commands.command(help = "Sent picture url to get picture exposure information.", brief = "Get picture exposure information.")
    async def exposure(self, ctx, pic_url):
        try:
            response = requests.get(pic_url)
        except IndexError:
            return await ctx.send('Image invalid!')
        file = open(os.path.join("..", "storage", "temp.jpg"), "wb")
        file.write(response.content)
        file.close()
        photo = io.imread(os.path.join("..", "storage", "temp.jpg"))
        R = plt.hist(photo[:,:,0].ravel(),bins=20,color='red',ec='red',histtype='step')
        G = plt.hist(photo[:,:,1].ravel(),bins=20,color='green',ec='green',histtype='step')
        B = plt.hist(photo[:,:,2].ravel(),bins=20,color='blue',ec='blue',histtype='step')
        plt.title('Exposure information')
        plt.savefig(os.path.join("..", "storage", "plt.png"))
        with open(os.path.join("..", "storage", "plt.png"), "rb") as f:
            picture = discord.File(f)
            await ctx.send(file = picture)

def setup(bot):
    bot.add_cog(Picture(bot))
