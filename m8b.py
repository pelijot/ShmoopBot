import discord
from dotenv import dotenv_values
import random
import os

config = dotenv_values(".env")

token = config.get("TOKEN")


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

    if message.content.startswith("<@1459293475127165070>"):
        lucky_num = random.randint(0,len(response_list) - 1)
        win_game = random.randint(0,10000)
        await message.reply(response_list[lucky_num])
        print(f"Replied '{response_list[lucky_num]}' ({lucky_num}) to @{message.author} [{win_game / 100}]")
        if win_game == 10000:
            await message.reply("You just won free access to the Steam (PC Version) of A Webbing Journey! Please contact <@701464203252203551>")



client.run("{}".format(token))


# https://github.com/justinbaur/m8b/tree/master
