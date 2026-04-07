import logging
import sys

import discord
from discord.ext import commands
from dotenv import dotenv_values

from m8b import Magic8Ball
from close import AutoClose

config = dotenv_values(".env")
token = config.get("TOKEN")


def setup_logging():
    formatter = logging.Formatter(
        fmt="[{asctime}] [{levelname}] [{name}] {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    # Quiet down discord.py's own verbose logging
    logging.getLogger("discord").setLevel(logging.WARNING)


def main():
    setup_logging()
    log = logging.getLogger("main")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        log.info(f"Logged in as {bot.user}")

    async def setup():
        await bot.add_cog(Magic8Ball(bot, config))
        await bot.add_cog(AutoClose(bot))

    bot.setup_hook = setup

    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
