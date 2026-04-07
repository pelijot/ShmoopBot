import logging
import math
import random
import time

from discord.ext import commands

log = logging.getLogger("m8b")

with open("response.list", "r") as f:
    response_list = [line.strip() for line in f if line.strip()]


def get_closeness(number, goal):
    difference = abs(number - goal)
    closeness_percent = (1 - difference / goal) * 100
    return math.trunc(closeness_percent)


class Magic8Ball(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.chance = int(config.get("WINCHANCE"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user not in message.mentions:
            return
        if message.author == self.bot.user and not message.content.startswith(f"<@{self.bot.application_id}>"):
            return
    
        response = random.choice(response_list)
        random_win = random.randint(1, self.chance)

        if random_win == self.chance:
            await message.reply(
                "You just won free access to the Steam (PC Version) of A Webbing Journey!"
                "Please contact <@701464203252203551>"
            )
            log.info(f"@{message.author} won [{get_closeness(random_win, self.chance)}%]")
            with open("win.log", "a") as winlog:
                winlog.write(
                    f"{message.author} (ID: {message.author.id}) on "
                    f"{time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())}\n"
                )
            return

        await message.reply(response)
        log.info(
            f"Replied '{response}' to @{message.author} "
            f"[{get_closeness(random_win, self.chance)}%]"
        )
