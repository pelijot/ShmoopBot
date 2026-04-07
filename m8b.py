import discord
from dotenv import dotenv_values
import random
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



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
#    if message.author == client.user:
#        return

    if client.user in message.mentions:
        lucky_num = random.randint(0,len(response_list) - 1)
        win_game = random.randint(0,chance)
        if win_game == chance:
            await message.reply("You just won free access to the Steam (PC Version) of A Webbing Journey! Please contact <@701464203252203551>")
            print(f"@{message.author} won [{win_game}%]")
            with open("win.log", "a") as winlog:
                winlog.write(f"{message.author} (ID: {message.author.id}) on {time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())}\n")
            return
        await message.reply(response_list[lucky_num])
        print(f"Replied '{response_list[lucky_num]}' ({lucky_num}) to @{message.author} [{win_game}%]")
       

client.run("{}".format(token))


# https://github.com/justinbaur/m8b/tree/master


