import logging
import random
import time


from discord.ext import commands

log = logging.getLogger("rps")



class RockPaperScissors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


        self.choices = ["rock", "paper", "scissors"]
        self.wins_against = {
            "rock": "scissors",
            "paper": "rock",
            "scissors": "paper"
        }



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return
        if self.bot.user not in message.mentions:
            return
        

        parts = message.content.lower().strip().split()

        if len(parts) == 2 and parts[1] in self.choices:
            
            user_choice = parts[1]
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
            await self.bot.process_commands(message)
            log.info(
                f"User: {user_choice} | Bot: {bot_choice} | Result: {result} (@{message.author})"
            )