import os
from discord import VoiceClient
from discord.ext import commands


class Voice(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.voice_client: VoiceClient | None = None

        if (str_id := os.getenv("DISCORD_ID")) is not None:
            self.DISCORD_ID = int(str_id)

    @commands.Cog.listener()
    # https://discordpy.readthedocs.io/en/stable/api.html#discord.on_voice_state_update
    async def on_voice_state_update(self, member, _before, after):
        member_id: int = member.id

        if member_id != self.DISCORD_ID:
            return

        if after.channel is not None:
            self.voice_client = await after.channel.connect()
        elif self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None

    @commands.command()
    async def join(self, ctx) -> None:
        pass
