import logging

import discord
from discord.ext import commands

log = logging.getLogger("close")

AUTO_CLOSE_TAGS = {"Answered", "Implemented", "Resolved", "Done!", "Done", "Solved", "Fixed"}


class AutoClose(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        log.info(f"{after} was updated")

        if not after.applied_tags:
            return
        if after.archived:
            log.info(f"{after} was already archived")
            return
        if after.locked:
            return

        tag_names = {tag.name for tag in after.applied_tags}

        if tag_names & AUTO_CLOSE_TAGS:
            matched_tags = ", ".join(tag_names & AUTO_CLOSE_TAGS)

            try:
                await after.edit(
                    archived=True,
                    reason=f"Auto-closed due to '{matched_tags}' tag",
                )
                log.info(f"Closed thread: {after}")
            except discord.Forbidden:
                log.error("Missing permissions to close thread.")
            except discord.HTTPException as e:
                log.error(f"Failed to close thread: {e}")
