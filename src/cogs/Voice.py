from os import getenv
from threading import Thread

from discord import FFmpegPCMAudio, VoiceClient
from discord.ext import commands
from speech_recognition import Microphone, Recognizer
import asyncio


class Voice(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.voice_client: VoiceClient | None = None

        if (str_id := getenv("DISCORD_ID")) is not None:
            self.DISCORD_ID = int(str_id)

        thread = Thread(target=self.listen_event)
        thread.daemon = True
        thread.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, _before, after) -> None:
        """
        Automatically joins and leaves call with the Discord user who's
        ID from `discord.Message.author.id` is the same as the DISCORD_ID
        environment variable.

        https://discordpy.readthedocs.io/en/stable/api.html#discord.on_voice_state_update
        """

        member_id: int = member.id

        # Do nothing if `member_id` does not match ID configured in the .env
        if member_id != self.DISCORD_ID:
            return

        # Join voice chat if matching user joins a new voice chat
        if after.channel is not None:
            self.voice_client = await after.channel.connect()

        # Disconnect from current voice client if matching user leaves
        elif self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None

    def listen_event(self):
        while True:
            recognizer = Recognizer()
            with Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                try:
                    text = recognizer.recognize_google(audio, language="ja-JP")
                    print(text)
                    if "クリス" in text:
                        asyncio.run(self.play(None))
                except:
                    pass



    @commands.command()
    async def play(self, ctx) -> None:
        audio_source = FFmpegPCMAudio(
            source="src/assets/voice/nani-yo.mp3", executable="/Users/dinh/.local/usr/bin/ffmpeg")

        if self.voice_client is not None:
            self.voice_client.play(audio_source)
