from .otogif import Otogif
import sqlite3

def setup(bot):
    bot.add_cog(Otogif(bot))
    conn = sqlite3.connect('gif_responder.db')
    bot = Otogif(bot, conn)
    bot.init_db()
    bot.add_cog(bot)