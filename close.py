import discord
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values(".env")

token= config.get("TOKEN")

AUTO_CLOSE_TAGS = {"Answered", "Implemented", "Resolved", "Done!", "Done", "Solved", "Fixed"}  # case-sensitive

intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_thread_update(before: discord.Thread, after: discord.Thread):
    print(f"{after} was updated")

    # Only forum threads have applied_tags
    if not after.applied_tags:
        return
    # Skip already archived threads
    if after.archived:
        print(f"{after} was already archived")
        return

    # If it was already locked, do nothing
    if after.locked:
        return

    # Get tag names
    tag_names = {tag.name for tag in after.applied_tags}

        # Check if ANY close tag is present
    if tag_names & AUTO_CLOSE_TAGS:
        matched_tags = ", ".join(tag_names & AUTO_CLOSE_TAGS)

        try:
            await after.edit(
                archived=True,
                reason=f"Auto-closed due to '{matched_tags}' tag"
            )
            print(f"Closed thread: {after} ")
        except discord.Forbidden:
            print("Missing permissions to close thread.")
        except discord.HTTPException as e:
            print(f"Failed to close thread: {e}")


bot.run(TOKEN)
