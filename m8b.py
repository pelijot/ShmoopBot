import discord
from dotenv import dotenv_values
import random
import math
import os
import time

config = dotenv_values(".env")

token = config.get("TOKEN")
chance = int(config.get("WINCHANCE"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

with open("response.list", "r") as f:
    response_list = [line.strip() for line in f if line.strip()]

print(response_list)

def get_closenesss(number, goal):
    difference = abs(number - goal)
    closeness_percent = (1 - difference / goal) * 100
    return math.trunc(closeness_percent)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
#    if message.author == client.user:
#        return

    if client.user in message.mentions:
        random_msg = random.randint(0,len(response_list) - 1)
        random_win = random.randint(1,chance)
        if random_win == chance:
            await message.reply("You just won free access to the Steam (PC Version) of A Webbing Journey! Please contact <@701464203252203551>")
            print(f"@{message.author} won [{get_closenesss(random_win, chance)}%]")
            with open("win.log", "a") as winlog:
                winlog.write(f"{message.author} (ID: {message.author.id}) on {time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())}\n")
            return
        await message.reply(response_list[random_msg])
        print(f"Replied '{response_list[random_msg]}' ({random_msg}) to @{message.author} [{get_closenesss(random_win, chance)}% {random_win}]")
       

client.run("{}".format(token))


# https://github.com/justinbaur/m8b/tree/master


