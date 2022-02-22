# Makise Kurisu Discord Bot

### Getting Started
#### Install from requirements.txt
```bash
python3 -m pip install -r requirements.txt
```

### Create .env file
`DISCORD_ID` - your discord id, found by printing out `discord.Message.author.id`\
`TOKEN` - The Discord Bot Token\
`PREFIX` - the prefix for commands\
`OPUS_PATH` - The path to libopus, not needed for Windows as opus is loaded automatically.\
    For Mac OS X, you can install opus with `brew install opus`.\
    The `OPUS_PATH` would then be `{HOMEBREW_PATH}/Cellar/opus/{VERSION}/lib/libopus.0.dylib`

#### Run Bot
```bash
python3 src/main.py
```
