import sqlite3, discord, __main__
from discord.ext import commands

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        mention = f'<@!{self.bot.user.id}>'
        if mention in message.content:
            await message.channel.send("Hello.")
            
    @commands.command()
    async def blacklist(self, ctx, arg=None):
        for x in __main__.blacklist:
            if x[0] == ctx.guild.id and x[1] == ctx.author.id:
                return False
        if not arg:
            return False
        elif len(arg) == 18:
            with __main__.DatabaseConnection() as dbinstance:
                dbcursor = dbinstance.cursor()
                dbcursor.execute('INSERT INTO Blacklist (userID, serverID) VALUES (?, ?)', (arg, ctx.guild.id))
                dbinstance.commit()
        else:
            return False

def setup(bot):
    bot.add_cog(Message(bot))