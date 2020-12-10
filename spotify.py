import discord, __main__, spotipy, sys
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = __main__.config['spotify_client_id'], client_secret=__main__.config['spotify_client_secret']))

    @commands.command()
    async def artist(self, ctx, arg=None):
        for x in __main__.blacklist:
            if x[0] == ctx.guild.id and x[1] == ctx.author.id:
                await ctx.send("<@"+str(ctx.author.id)+">, you are blacklisted from using the bot.")
                return False
        
        results = self.spotify.search(q='artist:' + arg, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            content = discord.Embed(
                color = 0x00FF00,
            )
            content.set_thumbnail(url = artist['images'][2]['url'])
            content.add_field(name = "Followers", value = artist['followers']['total'], inline = False)
            content.add_field(name = "Genre", value = artist['genres'][0], inline = False)
            content.add_field(name = "Popularity", value = artist['popularity'], inline = False)
            content.add_field(name = "Spotify URL", value = "[Click Here](" + artist['external_urls']['spotify'] + ")", inline = False)
            content.set_footer(text = "<"+artist['external_urls']['spotify']+">")
            content.set_author(name = artist['name'], icon_url = "https://cdn.discordapp.com/attachments/784835961137004599/786580481855455242/unknown.png")
            await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(Spotify(bot))