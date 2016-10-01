# shiritori-san
###A python bot for Discord, to play Shiritori!

The Shiritori-san bot was designed on a classic Japanese bot, originally [Harumoro](https://github.com/Harumoro) made this bot titled 'shiritori-kun'. It just simply didn't fit my needs as I wanted a bot that was made in Python (in comparison to his NodeJS). To sort this issue I made my own bot and added made it from square one attempting to retain as many features as possible from his bot. Also I made use of a checks.py created by [Rapptz](https://github.com/Rapptz)

[You can find his bot here.](https://github.com/Harumaro/shiritori-kun-discord-bot)
[You can find checks.py here.](https://github.com/Rapptz/RoboDanny/blob/master/cogs/utils/checks.py)

####Installation.

Quick note, you need to have Python 3.5+ to use this bot. And a basic knowledge of how to use Git.

1. Duplicate my code.
```git clone https://github.com/jakeoid/shiritori-san-discord-bot.git shiritori-san -b master```

2. Install the requirements in the requirements.txt.
```sudo -H pip3.5 install --upgrade -r requirements.txt```

3. Edit the settings inside of the bot
```nano bot.py```

4. Launch the bot.
```python3.5 bot.py```

####Usage.

> <word>

Simply type any word in Kana and the bot will intepret it. IF you want to chat without triggering the bot simply put a ~ before you speak!

> !currentletter, !letter, !kana, k

Shows you the current letter in play.

> !currentplayed, !currentwords

Shows you the words that have already been played and what not to repeat.

> !resetround

Votes to have the round reset! Currently set to vote out of /5

> !resetvotes

Shows the amount of votes you have in order to reset the round.

> !help

Shows you the rules of the game.

> !commands

Shows you the known commands.

####Moderator Usage.

For usage on my server I simply checked if the user had the ability to ban users, through this I allow them the permission to run the commands. If this doesn't suit you simply change the value.

> !reroll

Rerolls the current letter.

> !setletter <letter>

Set's the letter to <letter>

> !exportwords

Private Messages the staff member the letters (for a later feature).

####Customization.

This bot is currently lacking with the ability to customize itself, it will be added at a later date.

