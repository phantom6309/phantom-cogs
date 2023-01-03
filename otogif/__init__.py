from .otogif import Otogif
import sqlite3
conn = sqlite3.connect('gif_responder.db')
def setup(bot):
    bot.add_cog(Otogif(bot,conn))
    
    bot = Otogif(bot, conn)
    bot.init_db()
    