import discord
import checks
from discord.ext import commands
from random import randint
import random
import re

# ####################
# Bot description and command prefix.
# Alongside token and channel id.
# ####################

description = '''A bot that recreates the popular game of Shinitori on Discord.'''
bot = commands.Bot(command_prefix='!', description=description)

token = "";
botchannel = "";

# Variables
playedwords = [];
usersvoted = [];
roundresetvote = 0;

# Game Setup
currentletter = randHiragana()
lastplayer = ""

# Globals
global botchannel

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
# ####################

def randHiragana():

	hirachars = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'の',
	'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ', 'ら', 'り', 'る', 'れ', 'ろ', 'わ']
	
	num = randint(0,40)
	letter = hirachars[num]
	
	return letter;

# ####################
# Hiraganises the Katakana
# ####################

def katakanaToHiragana(str):

	# Replace Basic Kana

	output = str.replace("ア", "あ").replace("イ", "い").replace("ウ", "う").replace("エ", "え").replace("オ", "お").replace("カ", "か").replace("キ", "き").replace("ク", "く").replace("ケ", "け").replace("コ", "こ").replace("サ", "さ").replace("シ", "し").replace("ス", "す").replace("セ", "せ").replace("ソ", "そ").replace("タ", "た").replace("チ", "ち").replace("ツ", "つ").replace("テ", "て").replace("ト", "と").replace("ナ", "な").replace("ニ", "に").replace("ヌ", "ぬ").replace("ネ", "ね").replace("ノ", "の").replace("ハ", "は").replace("ヒ", "ひ").replace("フ", "ふ").replace("ヘ", "へ").replace("ホ", "ほ").replace("マ", "ま").replace("ミ", "み").replace("ム", "む").replace("メ", "め").replace("モ", "も").replace("ヤ", "や").replace("ユ", "ゆ").replace("ヨ", "よ").replace("ラ", "ら").replace("リ", "り").replace("ロ", "ろ").replace("レ", "れ").replace("ル", "る").replace("ワ", "わ").replace("ヲ", "を").replace("ン", "ん")

	# Replace Dakuten

	output = output.replace("ガ", "が").replace("ギ", "ぎ").replace("グ", "ぐ").replace("ゲ", "げ").replace("ゴ", "ご").replace("ザ", "ざ").replace("ジ", "じ").replace("ズ", "ず").replace("ゼ", "ぜ").replace("ゾ", "ぞ").replace("ダ", "だ").replace("ヂ", "ぢ").replace("ズ", "づ").replace("デ", "で").replace("ド", "ど").replace("バ", "ば").replace("ビ", "び").replace("ブ", "ぶ").replace("ベ", "べ").replace("ボ", "ぼ").replace("パ", "ぱ").replace("ピ", "ぴ").replace("プ", "ぷ").replace("ペ", "ぺ").replace("ポ", "ぽ")

	# Replace Small Kana

	output = output.replace("ャ", "ゃ").replace("ュ", "ゅ").replace("ョ", "ょ").replace("ァ", "ぁ").replace("ィ", "ぃ").replace("ゥ", "ぅ").replace("ェ", "ぇ").replace("ォ", "ぉ")

	return output;

# ####################
# Makes the small hiragana, larger.
# ####################

def removeSmallKana(str):

	output = str.replace("ゃ", "や").replace("ゅ", "ゆ").replace("ょ", "よ").replace("ぁ", "あ").replace("ぃ", "い").replace("ぅ", "う").replace("ぇ", "え").replace("ぉ", "お")

	return output;

# ####################
# Removes the default !help command
# because it sucks at explaining.
# ####################

bot.remove_command("help")

# ####################
# Shows you the rules of the game.
# ####################

@bot.command(pass_context=True)
async def help(ctx):
	await bot.send_message(discord.Object(id=botchannel), ":mailbox: | I have sent you a Private Message!")

	message = "```=== Shiritori Help ===```";
	message += "```Shiritori is a game about making words and expanding your vocabulary of any given language. The rules are simple and are as follows.\n\n";	
	message += "	1. Only nouns & adjectives are permitted. (rule of thumb is, anything ending in ます isn't allowed)\n";	
	message += "	2. Unlike the average game of Shiritori if a word ends with the 'ん' constanant, a new letter will be chosen.\n";	
	message += "	3. You are able to repeat words and/or use another word that a player has already played!```";	
	message += "```	To submit a word just type the word in kana!\n";
	message += "	If you want to speak in Japanese and not submit simply put 〜 at the start!\n";	
	message += "	To view all commands use !commands```";	

	await bot.send_message(ctx.message.author, message)

# ####################
# MODERATOR+ : Set's the current letter if broken.
# ####################

@bot.command(pass_context=True)
@checks.admin_or_permissions(ban_members=True)
async def setletter(ctx, userinput : str):
	global currentletter

	currentletter = userinput
	await bot.send_message(discord.Object(id=botchannel), ':blush: | I have set the letter to `' + userinput + "`")

# ####################
# MODERATOR+ : Export's out all of the words.
# ####################

@bot.command(pass_context=True)
@checks.admin_or_permissions(ban_members=True)
async def exportwords(ctx):
	global playedwords

	message = "The word's that are played are.. "

	for word in playedwords:
		message += word + " "

	await bot.send_message(discord.Object(id=botchannel), ":mailbox: | I have sent you a Private Message!")
	await bot.send_message(ctx.message.author, message)

# ####################
# MODERATOR+ : Rerolls our current letter.
# ####################

@bot.command(pass_context=True)
@checks.admin_or_permissions(ban_members=True)
async def reroll(ctx):
	global currentletter
	currentletter = randHiragana()
	await bot.send_message(discord.Object(id=botchannel), ":rofl: | The letter has been rerolled, it now is " + currentletter + ".")

# ####################
# Shows you the commands of the bot.
# ####################

@bot.command(pass_context=True)
async def commands(ctx):
	await bot.send_message(discord.Object(id=botchannel), ":mailbox: | I have sent you a Private Message!")

	message = "```=== Shiritori Command's List ===```";
	message += "```!currentletter \n 	# Shows the current letter being played!\n"	
	message += "!currentplayed \n 	# Shows the current already played words!\n"	
	message += "!help \n 	# Shows the rules of the game & how to play.\n"
	message += "!resetround \n 	# Votes to have the round reset!\n"		
	message += "!resetvotes \n 	# Shows the votes to have round reset!\n"
	message += "!commands \n 	# Shows this menu (duh!).```\n\n";	

	await bot.send_message(ctx.message.author, message)

# ####################
# Command to show current word's played.
# ####################

@bot.command()
async def currentplayed(aliases=["currentwords", "currentlyplayed", "currentplay"]):
	
	# Variables
	say = ""

	# Check if we have any words to show
	if(len(playedwords) > 0):
		# Setup a quick conversation.
		say = ":smile: | Currently, there is `" + str(len(playedwords)) + "` words played, they are.. "
		
		# Loop off every single word
		for letter in playedwords:
			say += letter + "\n"
	# We don't have any, don't show any.
	else:
		say = ":astonished: | No one has played any words yet, use `!shiritori <word>` to play one!"

	await bot.send_message(discord.Object(id=botchannel), say)

# ####################
# Command to show the current letter.
# ####################

@bot.command(aliases=["currentletter", "kana", "k"])
async def letter():
	await bot.send_message(discord.Object(id=botchannel), ":upside_down: | The current letter is " + currentletter + ".")

# ####################
# Views the amount of votes to have the round reset.
# ####################

@bot.command(pass_context=True)
async def resetvotes(ctx):
	await bot.send_message(discord.Object(id=botchannel), ":upside_down: | There is `" + str(roundresetvote) + "/5` votes to reset the round.")	

# ####################
# Tells the user that the command is no longer in use.
# ####################

@bot.command(pass_context=True)
async def shiritori(ctx):
	await bot.send_message(discord.Object(id=botchannel), ":upside_down: | This command is retired, simply just type the word now!")	

# ####################
# Sets your vote to have the round reset.
# ####################

@bot.command(pass_context=True)
async def resetround(ctx):
	# Globals
	global roundresetvote

	# Variables
	player = ctx.message.author.id

	# Don't let the user vote if they already have voted previously.
	if(str(player) in usersvoted):
		await bot.send_message(discord.Object(id=botchannel), ":upside_down: | You've already voted to have the round reset..")
		return

	# Upon this it will make it 10.
	if roundresetvote == 4:
		# Reset the counter
		roundresetvote = 0

		# Reset the player words
		playedwords[:] = []

		# Reset the players voted
		usersvoted[:] = []

		await bot.send_message(discord.Object(id=botchannel), ":star: | Ta-da~ The round was reset!")
	elif roundresetvote <= 9 & usersvoted.count(player) >= 0:
		# Adds one to the vote
		roundresetvote += 1

		# Adds the users name to the vote, so they cant do it again.
		usersvoted.append(str(ctx.message.author.id))

		# Tells the user amount of votes
		await bot.send_message(discord.Object(id=botchannel), ":upside_down: | You voted to have the round reset!")

# ####################

@bot.event
async def on_message(message):

	word = message.content
	user = message.author

	global currentletter
	global lastplayer

	checker = word[:2]

	# Remove hiragana & small kana
	fixedword = word
	fixedword = katakanaToHiragana(fixedword)
	fixedword = removeSmallKana(fixedword)

	ourletter = fixedword[:1]
	newletter = fixedword[-1:]

	player = message.author
	playername = message.author.name
	playerid = message.author.id

	# We don't want the bot to be replying to itself.

	if message.author == bot.user:
		return

	# Check that we are in the correct channel for #shiritori

	if message.channel.id == botchannel:
		await bot.process_commands(message)
	else:
		return

	# Check that the message contains Kana.

	pattern = "[^あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゔっゃょゅぁぃぅぇぉアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴッャョュァィゥェォー]+"
	string = message.content[:1]
	if not re.findall(pattern, string):
		# Check they weren't the last person to play.
		if lastplayer == playerid:
			await bot.send_message(discord.Object(id=botchannel), ":sweat_smile: | Sorry, but we can't let you play two words in a row!")
			print("WARN : " + playername + " tried to play a move twice. ")
			return

		# Check that the word hasn't already been played.
		if word in playedwords:
			await bot.send_message(discord.Object(id=botchannel), ":sweat_smile: | Sorry, but that word has already been played!")
			print("WARN : " + playername + " tried to play a move twice. ")
			return

		# Check that the letter is the same
		if (ourletter == currentletter) or (checker == "しゃ" and currentletter == "や"):

			# Update the playername for next time!
			lastplayer = playerid

			# Tell everyone about the new letter! (oh and print a debug message)
			await bot.send_message(discord.Object(id=botchannel), ":book: | A new word, `" + word + "` has been played by " + player.mention + ". The letter has now become `" + newletter + "`")
			print("INFO : " + playername + ' played ' + word + ", letter is now " + newletter)

			# Check that it doesn't end in 'ん'
			if newletter == "ん":
				# It ended in 'ん' so we re-roll a new hiragana.
				newletter = randHiragana();
				# Tell everyone excitedly and print a debug message.
				await bot.send_message(discord.Object(id=botchannel), ":sweat_smile: | Oh no! The word ended in `ん`! We've rolled the new letter `" + newletter + "`")
				print("WARN : The word ended in a `ん`!, It was then rolled to " + newletter)

			# Check that it doesn't end in 'ー'
			if newletter == "ー":
				# It ended in 'ん' so we re-roll a new hiragana.
				newletter = randHiragana();
				# Tell everyone excitedly and print a debug message.
				await bot.send_message(discord.Object(id=botchannel), ":sweat_smile: | Oh no! The word ended in `ー`! We've rolled the new letter `" + newletter + "`")
				print("WARN : The word ended in a `ー`!, It was then rolled to " + newletter)

			# Check that it doesn't end in 'っ'
			if newletter == "っ":
				# It ended in 'ん' so we re-roll a new hiragana.
				newletter = randHiragana();
				# Tell everyone excitedly and print a debug message.
				await bot.send_message(discord.Object(id=botchannel), ":sweat_smile: | Oh no! The word ended in `っ`! We've rolled the new letter `" + newletter + "`")
				print("WARN : The word ended in a `っ`!, It was then rolled to " + newletter)

			# Add the words to already played, thus we can't play it again.
			playedwords.append(word)

			# Set's the letter to show in 'playing'...
			newLetterGame = discord.Game()
			newLetterGame.name = "letter is " + newletter
			await bot.change_status(newLetterGame)

			# Update the current letter.
			currentletter = newletter

		else:
			# Tell the user that the letter isn't correct.
			await bot.send_message(discord.Object(id=botchannel), ":astonished: | `" + ourletter + '` is not the current letter, it\'s `' + currentletter + "`")
			print("WARN : " + playername + " tried to make an invalid move. ")


# ####################
# We start the bot using the token, token.
# ####################

bot.run(token)