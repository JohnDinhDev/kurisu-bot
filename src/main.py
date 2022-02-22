from os import getenv
from discord import Activity, ActivityType, Message, opus
from discord.ext import commands

from cogs.Voice import Voice
from dotenv import load_dotenv
from speech_recognition import AudioFile, Recognizer, Microphone

load_dotenv()  # load environment variables from .env file

# Loads libopus from .env if OPUS_PATH is defined.
if (opus_path := getenv("OPUS_PATH")) is not None:
    opus.load_opus(opus_path)

INITIAL_ACTIVITY = Activity(
    name="TINA じゃない！😡",
    type=ActivityType.playing)

bot = commands.Bot(
    command_prefix=getenv('PREFIX'),
    activity=INITIAL_ACTIVITY
)

bot.add_cog(Voice(bot))


@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}")


@bot.event
async def on_message(message: Message):
    """
    This overrides the default on_message event, requiring that we use
    `await bot.process_commands(message)` manually to process Cog commands.
    """
    print(f"Message from {message.author}: {message.content}")

    # https://discordpy.readthedocs.io/en/stable/api.html#discord.Member.bot
    if message.author.bot is True:  # type: ignore
        return

    if "jeff" in message.content.lower():
        await message.reply("<:jeff:650805353776414732>")

    await bot.process_commands(message)

bot.run(getenv('TOKEN'))
