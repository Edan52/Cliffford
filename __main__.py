import discord, json, asyncio, sqlite3, os.path
from discord.ext import commands

#Load config
with open("config.json", "r", encoding='utf-8') as json_file:
    config = json.load(json_file)

#Initialize database connection
class DatabaseConnection(object):

    def __enter__(self):
        self.dbconn = sqlite3.connect('database.db')
        return self.dbconn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()

print('------')
print('Initializing database...')
print('database file located, checking database...' if os.path.isfile('database.db') else 'database file not located, creating new database...')

with DatabaseConnection() as dbinstance:
    dbcursor = dbinstance.cursor()
    dbcursor.execute("""CREATE TABLE IF NOT EXISTS Blacklist (
	            userID INTEGER,
	            serverID INTEGER
                );""")
    dbinstance.commit()
    dbcursor.execute('SELECT serverID, userID FROM Blacklist')
    blacklist = dbcursor.fetchall()

#Initializing the bot
bot = commands.Bot(command_prefix=config['bot_command'])

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="YOU"))

#Load extensions here
bot.load_extension('message')
if config['spotify_enabled']: #Enable in config
    bot.load_extension('spotify')
bot.run(config['bot_token'])