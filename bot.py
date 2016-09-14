import discord
from discord.ext import commands
from random import randint
import random

# ####################
# Bot description and command prefix.
# ####################

description = '''A bot that recreates the popular game of Shinitori on Discord.'''
bot = commands.Bot(command_prefix='!', description=description)
token = "";
botchannel = "";

playedwords = [];

# ####################
# Debugging messages.
# ####################

@bot.event
async def on_ready():
	print('Logged in as')
	print('')
	print(bot.user.name)
	print(bot.user.id)
	print('')
	print('------')

# ####################
# Generates a random hiragana
# character in the case of 'ん'
# & character in the case of game start.
# ####################

def randHiragana():

	letter = ""
	num = randint(1,45)

	if(num == 1):
		letter = "あ"
	if(num == 2):
		letter = "い"
	if(num == 3):
		letter = "う"
	if(num == 4):
		letter = "え"
	if(num == 5):
		letter = "お"
	if(num == 6):
		letter = "か"
	if(num == 7):
		letter = "き"
	if(num == 8):
		letter = "く"
	if(num == 9):
		letter = "け"
	if(num == 10):
		letter = "こ"
	if(num == 11):
		letter = "さ"
	if(num == 12):
		letter = "し"
	if(num == 13):
		letter = "す"
	if(num == 14):
		letter = "せ"
	if(num == 15):
		letter = "た"
	if(num == 16):
		letter = "ち"
	if(num == 17):
		letter = "つ"
	if(num == 18):
		letter = "て"
	if(num == 19):
		letter = "と"
	if(num == 20):
		letter = "な"
	if(num == 21):
		letter = "に"
	if(num == 22):
		letter = "ぬ"
	if(num == 23):
		letter = "ね"
	if(num == 24):
		letter = "の"
	if(num == 25):
		letter = "は"
	if(num == 26):
		letter = "ひ"
	if(num == 27):
		letter = "ふ"
	if(num == 28):
		letter = "へ"
	if(num == 29):
		letter = "ほ"
	if(num == 30):
		letter = "ま"
	if(num == 31):
		letter = "み"
	if(num == 32):
		letter = "む"
	if(num == 33):
		letter = "め"
	if(num == 34):
		letter = "も"
	if(num == 35):
		letter = "や"
	if(num == 36):
		letter = "ゆ"
	if(num == 37):
		letter = "よ"
	if(num == 38):
		letter = "ら"
	if(num == 39):
		letter = "り"
	if(num == 40):
		letter = "る"
	if(num == 41):
		letter = "れ"
	if(num == 42):
		letter = "ろ"
	if(num == 43):
		letter = "わ"
	if(num == 44):
		letter = "を"
	if(num == 45):
		letter = "そ"

	return letter;

# ####################
# Defining a random character
# and who played last.
# ####################

currentletter = randHiragana()
lastplayer = ""

# ####################
# Removes the default !help command
# because they suck.
# ####################

bot.remove_command("help")

# ####################
# Makes sure that we are only pulling
# from the channel #shiritori.
# ####################

@bot.event
async def on_message(m):
	if m.channel.id == '225567870011047936':
		await bot.process_commands(m)

# ####################
# Shows you how to play.
# And the rules of the game.
# ####################

@bot.command()
async def help():
	message = "__**SHIRITORI RULES AND HELP**__\n\n";
	message += "Shiritori is a game about making words and expanding your vocabulary of any given language. The rules are simple and are as follows.";	
	message += "\n\n1. Only nouns are permitted.";	
	message += "\n2. If you submit a word ending in 'ん' it will be replaced.";	
	message += "\n3. Words may not be repeated.";	
	message += "\n\nTo submit a word use `!shiritori <word>`!";	

	await bot.say(message)

# ####################
# TODO
# Implement a message for
# when the bot starts and
# goes offline.
#
# '"I HAVE AWOKEN MORTALS"'
# '"PLAY SHIRITORI OR DIE"'
# #####################

# ####################
# Command to show current word's played.
# ####################

@bot.command()
async def currentlyplayed(aliases=["currentwords"]):
	say = "The currently played words are.. "
	say += "".join(playedwords) + ","

	await bot.say(say + ".");

# ####################
# Command to show the current letter.
# ####################

@bot.command(aliases=["currentletter", "kana", "k"])
async def letter():
	await bot.say("The current letter is " + currentletter + ".")

# ####################
# TODO 
# Ends the current match resetting
# the current words that are played.
# ####################

# ####################
# Command to play words.
# ####################

@bot.command(pass_context=True)
async def shiritori(ctx, word : str):
	"""Allows you to submit a word to a game of Shiritori"""

	# Defining our current letter
	global currentletter
	# Grabbing the player
	global lastplayer
	# New letter.
	ourletter = word[:1]
	# New last character
	newletter = word[-1:]
	
	# Getting some stuff about our player.
	player = ctx.message.author
	playername = ctx.message.author.name

	# Check they weren't the last person to play.
	if lastplayer == playername:
		await bot.say("Sorry, but we can't let you play two words in a row!")
		return

		# ####################
		# TODO: Check that all the characters are Hiragana.
		# ####################

		# ####################
		# TODO: Convert all the text to Hiragana.
		# ####################

	# Check that the letter is the same
	if ourletter == currentletter:

		# Update the playername for next time!
		lastplayer = playername

		# Tell everyone about the new letter!
		await bot.say("A new word, `" + word + "` has been played by " + ctx.message.author.mention + ". The letter has now become `" + newletter + "`")
		print("INFO : " + playername + ' played ' + word + ", letter is now " + newletter)

		# Check that it doesn't end in 'ん'
		if newletter == "ん":
			# It ended in 'ん' so we re-roll a new hiragana.
			newletter = randHiragana();
			# Tell everyone excitedly.
			await bot.say("Oh no! The word ended in `ん`! We've rolled the new letter `" + newletter + "`")
			print("WARN : The word ended in a `ん`!, It was then rolled to " + newletter)

		playedwords.append(word)

		currentletter = newletter

	# Boo-hoo, it wasn't tell them.
	else:
		await bot.say("`" + ourletter + '` is not the current letter, it\'s `' + currentletter + "`")

# ####################
# TODO: Check that all arguments are met.
# ####################

bot.run(token)