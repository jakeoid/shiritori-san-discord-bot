import discord
from discord.ext import commands
from random import randint
import random
import re

# ####################
# Bot description and command prefix.
# ####################

description = '''A bot that recreates the popular game of Shinitori on Discord.'''
bot = commands.Bot(command_prefix='!', description=description)

playedwords = [];

usersvoted = [];
roundresetvote = 0;

token = "";
botchannel = "";


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

	hirachars = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'の',
	'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を']
	
	num = randint(1,45)
	letter = hirachars[num]
	
	return letter;

# ####################
# Replaces all the Katakana characters 
# with their Hiragana counterpart.
# ####################

def katakanaToHiragana(str):

	# Replace Basic Kana

	output = str.replace("ア", "あ").replace("イ", "い").replace("ウ", "う").replace("エ", "え").replace("オ", "お").replace("カ", "か").replace("キ", "き").replace("ク", "く").replace("ケ", "け").replace("コ", "こ").replace("サ", "さ").replace("シ", "し").replace("ス", "す").replace("セ", "せ").replace("ソ", "そ").replace("タ", "た").replace("チ", "ち").replace("ツ", "つ").replace("テ", "て").replace("ト", "と").replace("ナ", "な").replace("ニ", "に").replace("ヌ", "ぬ").replace("ネ", "ね").replace("ノ", "の").replace("ハ", "は").replace("ヒ", "ひ").replace("フ", "ふ").replace("ヘ", "へ").replace("ホ", "ほ").replace("マ", "ま").replace("ミ", "み").replace("ム", "む").replace("メ", "め").replace("モ", "も").replace("ヤ", "や").replace("ユ", "ゆ").replace("ヨ", "よ").replace("ラ", "ら").replace("リ", "り").replace("ロ", "る").replace("レ", "れ").replace("ル", "ろ").replace("ワ", "わ").replace("ヲ", "を").replace("ン", "ん")

	# Replace Dakuten

	output = output.replace("ガ", "が").replace("ギ", "ぎ").replace("グ", "ぐ").replace("ゲ", "げ").replace("ゴ", "ご").replace("ザ", "ざ").replace("ジ", "じ").replace("ズ", "ず").replace("ゼ", "ぜ").replace("ゾ", "ぞ").replace("ダ", "だ").replace("ヂ", "ぢ").replace("ズ", "づ").replace("デ", "で").replace("ド", "ど").replace("バ", "ば").replace("ビ", "び").replace("ブ", "ぶ").replace("ベ", "べ").replace("ボ", "ぼ").replace("パ", "ぱ").replace("ピ", "ぴ").replace("プ", "ぷ").replace("ペ", "ぺ").replace("ポ", "ぽ")

	# Replace Small Kana

	output = output.replace("ャ", "ゃ").replace("ュ", "ゅ").replace("ョ", "ょ").replace("ァ", "ぁ").replace("ィ", "ぃ").replace("ゥ", "ぅ").replace("ェ", "ぇ").replace("ォ", "ぉ")

	return output;

# ####################
# Replaces all the small Kana
# with their larger counterpart.
# ####################

def removeSmallKana(str):

	output = str.replace("ゃ", "や").replace("ゅ", "ゆ").replace("ょ", "よ").replace("ぁ", "あ").replace("ぃ", "い").replace("ぅ", "う").replace("ぇ", "え").replace("ぉ", "お")

	return output;

# ####################
# Defining a random character
# and who played last.
# ####################

currentletter = randHiragana()
lastplayer = ""

# ####################
# Removes the default !help command
# because it sucks at explaining.
# ####################

bot.remove_command("help")

# ####################
# Makes sure that we are only pulling
# from the channel #shiritori.
# ####################

@bot.event
async def on_message(m):
	global botchannel
	if m.channel.id == botchannel:
		await bot.process_commands(m)

# ####################
# Shows you the rules of the game.
# ####################

@bot.command()
async def help():
	message = "__**RULES AND HELP**__\n\n";
	message += "Shiritori is a game about making words and expanding your vocabulary of any given language. The rules are simple and are as follows.";	
	message += "\n\n1. Only nouns & adjectives are permitted.";	
	message += "\n2. If you submit a word ending in 'ん' it will be replaced.";	
	message += "\n3. Words may not be repeated.";	
	message += "\n\nTo submit a word use `!shiritori <word>`";	
	message += "\n\nTo view all commands use `!commands`";	

	await bot.say(message)

# ####################
# Shows you the commands of the bot.
# ####################

@bot.command()
async def commands():
	message = "__**COMMANDS**__\n\n";
	message += "`!shiritori <word>` - Submits your word to the Shiritori game!\n";	
	message += "`!currentletter` - Shows the current letter being played!\n";	
	message += "`!currentplayed` - Shows the current already played words!\n";	
	message += "`!help` - Shows the rules of the game & how to play.\n";		
	message += "`!commands` - Shows this menu (duh!).\n\n";	

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
# Reset round.
# ####################

@bot.command(pass_context=True)
async def resetround(ctx):
	global roundresetvote

	player = ctx.message.author.name

	# Upon this it will make it 10.
	if roundresetvote == 9:
		# Reset the counter
		roundresetvote = 0

		# Reset the player words
		playedwords[:] = []

		# Reset the players voted
		usersvoted[:] = []
	elif roundresetvote <= 9 & usersvoted.count(player) >= 0:
		# Adds one to the vote
		roundresetvote += 1

		# Adds the users name to the vote, so they cant do it again.
		usersvoted.append(ctx.message.author.name)

		# Tells the user amount of votes
		await bot.say("You voted to have the round reset!")

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

	# Remove hiragana & small kana
	fixedword = word
	fixedword = katakanaToHiragana(fixedword)
	fixedword = removeSmallKana(fixedword)

	# New letter.
	ourletter = fixedword[:1]
	# New last character
	newletter = fixedword[-1:]

	pattern = "[^あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃょゅぁぃぅぇぉー]+"
	string = word
	if re.findall(pattern, string):
		await bot.say("Aaah! Your word contained invalid characters! You can only use Kana to submit.. sorry.")
		return

	# Getting some stuff about our player.
	player = ctx.message.author
	playername = ctx.message.author.name

	# Check they weren't the last person to play.
	if lastplayer == playername:
		await bot.say("Sorry, but we can't let you play two words in a row!")
		print("WARN : " + playername + " tried to play a move twice. ")
		return

	# Check that the letter is the same
	if ourletter == currentletter:

		# Update the playername for next time!
		lastplayer = playername

		# Tell everyone about the new letter! (oh and print a debug message)
		await bot.say("A new word, `" + word + "` has been played by " + ctx.message.author.mention + ". The letter has now become `" + newletter + "`")
		print("INFO : " + playername + ' played ' + word + ", letter is now " + newletter)

		# Check that it doesn't end in 'ん'
		if newletter == "ん":
			# It ended in 'ん' so we re-roll a new hiragana.
			newletter = randHiragana();
			# Tell everyone excitedly and print a debug message.
			await bot.say("Oh no! The word ended in `ん`! We've rolled the new letter `" + newletter + "`")
			print("WARN : The word ended in a `ん`!, It was then rolled to " + newletter)

			playedwords.append(word)

		currentletter = newletter

	# Boo-hoo, it wasn't tell them.
	else:
		await bot.say("`" + ourletter + '` is not the current letter, it\'s `' + currentletter + "`")
		print("WARN : " + player + " tried to make an invalid move. ")

bot.run(token)