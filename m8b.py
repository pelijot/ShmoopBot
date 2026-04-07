import logging
import math
import random
import time

import aiohttp
from discord.ext import commands

log = logging.getLogger("m8b")


def get_closeness(number, goal):
    difference = abs(number - goal)
    closeness_percent = (1 - difference / goal) * 100
    return math.trunc(closeness_percent)


async def load_responses(config):
    online = config.get("RS_ONLINE", "false").lower() == "true"
    location = config.get("RS_LOCATION", "response.list")

    if online:
        log.info(f"Fetching response list from {location}")
        async with aiohttp.ClientSession() as session:
            async with session.get(location) as resp:
                resp.raise_for_status()
                text = await resp.text()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
    else:
        log.info(f"Loading response list from local file: {location}")
        with open(location, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

    log.info(f"Loaded {len(lines)} responses")
    return lines


class Magic8Ball(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.response_list = []
        self.special = config.get("SPECIAL", "false").lower() == "true"
        self.chance = int(config.get("SPECIAL_CHANCE", "1000"))

    async def reload(self, config):
        self.special = config.get("SPECIAL", "false").lower() == "true"
        self.chance = int(config.get("SPECIAL_CHANCE", "1000"))
        self.response_list = await load_responses(config)

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user not in message.mentions:
            return
        if message.author == self.bot.user:
            return
        if not self.response_list:
            log.warning("Response list is empty, skipping reply")
            return

        response = random.choice(self.response_list)
        random_win = random.randint(1, self.chance)

        if self.special and random_win == self.chance:
            await message.reply(
                "Shmoop"
                "(this message is a 1 in 1000)"
            )
            log.info(f"@{message.author} won [{get_closeness(random_win, self.chance)}%]")
            with open("win.log", "a") as winlog:
                winlog.write(
                    f"{message.author} (ID: {message.author.id}) on "
                    f"{time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())}\n"
                )
            return

        await message.reply(response)
        await self.bot.process_commands(message)
        log.info(
            f"Replied '{response}' to @{message.author} "
            f"[{get_closeness(random_win, self.chance)}%]"
        )
