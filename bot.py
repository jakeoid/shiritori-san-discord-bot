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

token = "MjI2MTA1NzgzMzU0MzkyNTg2.Cryw8A.d1AwFyA2RwTl_od_4OGR0h3Rn8s";
global botchannel
botchannel = "269767889001775104";

# Variables
playedwords = []

# Game Setup
currentletter = ""
lastplayer = ""

# Globals

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

currentletter = randHiragana()

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
	em = discord.Embed(colour=0xF44336)
	em.add_field(name='Shiritori Rules!', value='Because you\'re gonna have a badtime otherwise!', inline='false')
	em.add_field(name='1.', value='Nouns & adjectives are permitted.', inline='true')
	em.add_field(name='2.', value='Words ending a \'ん\', will be rolled.', inline='true')
	em.add_field(name='3.', value='You cannot replay words.', inline='true')
	em.add_field(name='4.', value='Have fun (or else).', inline='true')
	em.add_field(name='The idea is to take the previous words last letter & and use it in a new one!', value='To submit a word just type the word in kana and the bot should pick it up!', inline='false')

	await bot.send_message(ctx.message.channel, "", embed=em)

# ####################
# Shows you the commands of the bot.
# ####################

@bot.command(pass_context=True)
async def commands(ctx):
	em = discord.Embed(colour=0xF44336)
	em.add_field(name='Shiritori Commands!', value='HOW DO I CONTROL THIS AAAAAAA!!1!', inline='false')
	em.add_field(name='!currentplayed', value='Shows played words!', inline='true')
	em.add_field(name='!help', value='Shows the rules!', inline='true')
	em.add_field(name='!commands', value='Shows this menu!', inline='true')

	await bot.send_message(ctx.message.channel, "", embed=em)

# ####################
# MODERATOR+ : Set's the current letter if broken.
# ####################

@bot.command(pass_context=True)
@checks.admin_or_permissions(ban_members=True)
async def setletter(ctx, userinput : str):
	global currentletter

	currentletter = userinput
	
	em = discord.Embed(colour=0xF44336)
	em.add_field(name='A new letter has been set!', value='The new letter is now.. ' + userinput, inline='false')
	await bot.send_message(ctx.message.channel, "", embed=em)

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

	await bot.send_message(ctx.message.author, message)

# ####################
# MODERATOR+ : Rerolls our current letter.
# ####################

@bot.command(pass_context=True)
@checks.admin_or_permissions(ban_members=True)
async def reroll(ctx):
	global currentletter
	currentletter = randHiragana()

	em = discord.Embed(colour=0xF44336)
	em.add_field(name='Woah! The letter was rerolled!', value='The new letter is now.. ' + currentletter, inline='false')
	await bot.send_message(ctx.message.channel, "", embed=em)

# ####################
# Command to show current word's played.
# ####################

@bot.command(pass_context=True)
async def currentplayed(ctx, aliases=["currentwords", "currentlyplayed", "currentplay"]):
	
	# Variables
	say = ""

	em = discord.Embed(colour=0xF44336)

	# Check if we have any words to show
	if(len(playedwords) > 0):
		# Setup a quick conversation.
		em.add_field(name='Currently played words are..', value="There is `" + str(len(playedwords)) + "` words played.", inline='false')
		
		# Loop off every single word
		for letter in playedwords:
			say += letter + "\n"

		# oh god
		em.add_field(name='They are.. ', value='' + say)
	# We don't have any, don't show any.
	else:
		em.add_field(name='Currently played words are...', value="Uh.. oh, theres no words played! Current letter is " + currentletter, inline='false')

	await bot.send_message(ctx.message.channel, "", embed=em)

# ####################
# Command to show the current letter.
# ####################

@bot.command(pass_context=True, aliases=["currentletter", "kana", "k"])
async def letter(ctx):
	em = discord.Embed(colour=0xF44336)
	em.add_field(name='You\'re gonna struggle if you dont know the letter!', value="Luckily I know what it is! Current letter is `" + currentletter + "`", inline='false')
	await bot.send_message(ctx.message.channel, "", embed=em)

# ####################

@bot.event
async def on_message(message):

	word = message.content
	user = message.author

	em = discord.Embed(colour=0xF44336)

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
			em.add_field(name='Woops, thats not good.', value="You can't play twice in a row, that'd be dumb.", inline='false')
			print("WARN : " + playername + " tried to play a move twice. ")
			await bot.send_message(message.channel, "", embed=em)
			return

		# Check that the word hasn't already been played.
		if word in playedwords:
			em.add_field(name='Woops, thats not good.', value="Sorry, that words already been played.", inline='false')
			print("WARN : " + playername + " tried to play a word twice. ")
			await bot.send_message(message.channel, "", embed=em)
			return

		# Check that the letter is the same
		if (ourletter == currentletter) or (checker == "しゃ" and currentletter == "や"):

			# Update the playername for next time!
			lastplayer = playerid

			# Tell everyone about the new letter! (oh and print a debug message)
			em.add_field(name="A new word, `" + word + "` has been played by " + playername, value="The letter has now become `" + newletter + "`", inline='false')
			print("INFO : " + playername + ' played ' + word + ", letter is now " + newletter)

			# Check that it doesn't end in 'ん'
			if newletter == "ん":
				# It ended in 'ん' so we re-roll a new hiragana.
				newletter = randHiragana();
				# Tell everyone excitedly and print a debug message.
				em.add_field(name="Woops, theres an issue!", value="Oh no! The word ended in `ん`! We've rolled the new letter `" + newletter + "`", inline='false')
				print("WARN : The word ended in a `ん`!, It was then rolled to " + newletter)

			# Check that it doesn't end in 'ー'
			if newletter == "ー":
				# It ended in 'ん' so we re-roll a new hiragana.
				newletter = randHiragana();
				# Tell everyone excitedly and print a debug message.
				em.add_field(name="Woops, theres an issue!", value="Oh no! The word ended in `ー`! We've rolled the new letter `" + newletter + "`", inline='false')
				print("WARN : The word ended in a `ー`!, It was then rolled to " + newletter)

			# Check that it doesn't end in 'っ'
			if newletter == "っ":
				# It ended in 'ん' so we re-roll a new hiragana.
				newletter = randHiragana();
				# Tell everyone excitedly and print a debug message.
				em.add_field(name="Woops, theres an issue!", value="Oh no! The word ended in `っ`! We've rolled the new letter `" + newletter + "`", inline='false')
				print("WARN : The word ended in a `っ`!, It was then rolled to " + newletter)

			# Send message
			await bot.send_message(message.channel, "", embed=em)

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
			em.add_field(name="`" + ourletter + "` is not the current letter!", value="The current letter is `" + currentletter + "`!", inline='false')
			await bot.send_message(message.channel, "", embed=em)
			# Print a debug message.
			print("WARN : " + playername + " tried to make an invalid move. ")


# ####################
# We start the bot using the token, token.
# ####################

bot.run(token)