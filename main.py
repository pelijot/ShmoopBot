import asyncio
import logging
import sys

import discord
from discord.ext import commands
from dotenv import dotenv_values

from m8b import Magic8Ball, load_responses
from close import AutoClose
from rps import RockPaperScissors

log = logging.getLogger("main")


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

    logging.getLogger("discord").setLevel(logging.WARNING)


async def reload_all(bot):
    config = dotenv_values(".env")
    log.info("Reloading config and response list...")

    m8b_cog = bot.get_cog("Magic8Ball")
    if m8b_cog:
        await m8b_cog.reload(config)

    log.info("Reload complete")


async def stdin_listener(bot):
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        key = line.strip().lower()
        if key == "r":
            await reload_all(bot)


def main():
    setup_logging()

    config = dotenv_values(".env")
    token = config.get("TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        log.info(f"Logged in as {bot.user}")

    async def setup():
        m8b = Magic8Ball(bot, config)
        m8b.response_list = await load_responses(config)
        await bot.add_cog(m8b)
        await bot.add_cog(RockPaperScissors(bot))
        await bot.add_cog(AutoClose(bot))
        bot.loop.create_task(stdin_listener(bot))

    bot.setup_hook = setup

    bot.run(token, log_handler=None)


if __name__ == "__main__":
    main()
