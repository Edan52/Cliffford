import discord, __main__, spotipy, sys
from discord.ext import commands
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(__main__.config['spotify_client_id'], client_secret=__main__.config['spotify_client_secret']))

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
            await ctx.send(artist['images'][0]['url'])

def setup(bot):
    bot.add_cog(Spotify(bot))