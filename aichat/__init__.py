from .aichat import AIChat

def setup(bot):
    bot.add_cog(AIChat(bot))
