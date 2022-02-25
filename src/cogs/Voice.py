import asyncio
from os import getenv
from threading import Thread

from discord import AudioSource, FFmpegPCMAudio, VoiceClient
from discord.ext import commands
from speech_recognition import Microphone, Recognizer


class Voice(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.voice_client: VoiceClient | None = None

        self.recognizer = Recognizer()
        self.mic = Microphone()

        self.recognizer.energy_threshold = 1500

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

        # Join voice chat if matching user joins a new voice chat.
        if after.channel is not None:

            # Disconnect from current voice chat if user moved to a new voice chat.
            if self.voice_client is not None:
                await self.voice_client.disconnect()

            # Connects to voice chat user just joined.
            self.voice_client = await after.channel.connect()

        # Disconnect from current voice client if matching user leaves.
        elif self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None

    def listen_event(self):
        with self.mic as mic:
            while True:
                self.recognizer.adjust_for_ambient_noise(
                    self.mic, duration=0.5)
                audio = self.recognizer.listen(mic)
                try:
                    print("trying")
                    text = self.recognizer.recognize_google(
                        audio, language="ja-JP")
                    print(text)
                    if "ティーナ" in text or "ティナ" in text:
                        audio_source = FFmpegPCMAudio(
                            source="src/assets/voice/mad-scientist.mp3")
                        self.play_audio(audio_source)
                    elif "クリス" == text or "もしもし" in text:
                        audio_source = FFmpegPCMAudio(
                            source="src/assets/voice/nani-yo.mp3")
                        self.play_audio(audio_source)
                    elif "ツンデレ" in text or "シンデレ" in text:
                        audio_source = FFmpegPCMAudio(
                            source="src/assets/voice/dare-ga-tsundere-da.mp3")
                        self.play_audio(audio_source)
                except:
                    print("Could not understand.")
                finally:
                    text = ""

    def play_audio(self, audio_source: AudioSource):
        if self.voice_client is not None:
            self.voice_client.play(audio_source)

    @commands.command(name="play")
    async def play_command(self, ctx) -> None:
        audio_source = FFmpegPCMAudio(
            source="src/assets/voice/nani-yo.mp3")

        if self.voice_client is not None:
            self.voice_client.play(audio_source)
