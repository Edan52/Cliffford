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
                await ctx.send("<@"+str(ctx.author.id)+">, you are blacklisted from using the bot.")
                return False
        if ctx.message.author.guild_permissions.administrator:
            if not arg:
                await ctx.send("<@"+str(ctx.author.id)+">, please specify arguments.")
                return False
            elif len(arg) == 18:
                with __main__.DatabaseConnection() as dbinstance:
                    try:
                        dbcursor = dbinstance.cursor()
                        dbcursor.execute('INSERT INTO Blacklist (userID, serverID) VALUES (?, ?)', (arg, ctx.guild.id))
                        dbinstance.commit()
                        __main__.blacklist.append([int(arg), ctx.guild.id])
                        print(__main__.blacklist)
                        return True
                    except Exception:
                        await ctx.send("<@"+str(ctx.author.id)+">, please provide a discord ID.")
            else:
                await ctx.send("<@"+str(ctx.author.id)+">, please provide a discord ID.")
                return False
        else:
            await ctx.send("<@"+str(ctx.author.id)+">, you do not have permission to use this command.")
            return False

def setup(bot):
    bot.add_cog(Message(bot))