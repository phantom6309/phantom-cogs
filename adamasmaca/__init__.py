from .adamasmaca import Adamasmaca
from redbot.core import data_manager


def setup(bot):
    n = Adamasmaca(bot)
    data_manager.bundled_data_path(n)
    bot.add_cog(n)
