import logging
import random
import time


from discord.ext import commands

log = logging.getLogger("rps")



class RockPaperScissors(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot


        self.choises = ["rock", "paper", "scissors"]
        self.wins_against = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        content = message.content.lower()

        if content.startswith(tuple(self.choices)):

            user_choice = next(
                choice for choice in self.choices if content.startswith(choice)
            )

            bot_choice = random.choice(self.choices)

            if user_choice == bot_choice:
                result = "It's a draw!"
            elif self.wins_against[user_choice] == bot_choice:
                result = "You win!"
            else:
                result = "You lose!"

            await message.reply(
                f"I chose **{bot_choice}**\n"
                f"{result}"
            )

            log.info(
                f"User: {user_choice} | Bot: {bot_choice} | Result: {result} (@{message.author})"
            )