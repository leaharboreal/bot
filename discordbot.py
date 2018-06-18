#############
#           #
#    Bot    #
#           #
#############

# Written badly by ShiftyWizard

#Importing Requirements
import discord
import asyncio
import random
import os
import traceback
import re
from hyphenate import hyphenate_word
import nltk
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import urllib.request
import json 
import shutil

#Set working directory to file's location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

client = discord.Client()
prefix = "."
txtin = ""
txtout = ""
synonyms = []
sid = SentimentIntensityAnalyzer()

#Compile regex for xkcd37
xkcd37 = re.compile(r"(\w)-ass (\w)", re.MULTILINE)
xkcd37sub = "\\1 ass-\\2"

@client.event
async def on_ready():
	print("Account: "+client.user.name)
	print("Account ID: "+client.user.id)
	print("Bot Account: "+str(client.user.bot))
	print("||||||||| ONLINE |||||||||")
#
@client.event
async def on_message(message):
	if not client.user.id == message.author.id:
		if not os.path.isfile(os.path.join('settings',str(message.server.id+'.json'))):
			shutil.copy2('settings.json', os.path.join('settings',str(message.server.id+'.json')))
			print("created "+str(os.path.join('settings',str(message.server.id+'.json'))))
		with open(os.path.join('settings',str(message.server.id+'.json')),'r') as serversettings:
			settings = json.loads(serversettings.read())
			prefix = str(settings["bot"]["prefix"])
			global txtout

			#.test#
			if message.content.lower().startswith(prefix+settings["commands"]["test"]["command"]) and settings["commands"]["test"]["enabled"]==True:
				print(':robot:')
				await client.send_message(message.channel, ':robot:')
			
			#.info#
			elif message.content.lower().startswith(prefix+settings["commands"]["info"]["command"]) and settings["commands"]["info"]["enabled"]==True:
				print('BOT INFO')
				embed = discord.Embed(title="BOT INFO", description="Made by @ShiftyWizard#4823 & @Arboreal#4200 for fun.", url="https://github.com/leaharboreal/bot", color=0x1abc9c)
				embed.set_thumbnail(url="https://raw.githubusercontent.com/leaharboreal/bot/master/profilepic.png")
				embed.set_footer(text="© bot | 2018", icon_url="https://raw.githubusercontent.com/leaharboreal/bot/master/profilepic.png")
				await client.send_message(message.channel, embed=embed)

			#.addquote#
			elif message.content.lower().startswith(prefix+settings["commands"]["addquote"]["command"]) and settings["commands"]["addquote"]["enabled"]==True:
				f = open(os.path.join('quotes',str(message.server.id+'.txt')),'a+')
				quotemessage = message.content[10:].split("|")
				f.write(quotemessage[0] + "|" + quotemessage[1]+'\n')
				print("Added Quote to file "+message.server.id+".txt: "+str(quotemessage))
				await client.send_message(message.channel,":white_check_mark:")
				f.close()
			
			#.quote#
			elif message.content.lower().startswith(prefix+settings["commands"]["quote"]["command"]) and settings["commands"]["quote"]["enabled"]==True:
				try:
					f = open(os.path.join('quotes',str(message.server.id+'.txt')),'r')
					quotes = []
					quote = []

					for line in f:
						if "|" in line:
							if len(message.content) > 7:
								if str(line).split("|")[0].lower() == message.content.lower()[7:]:
									quotes.append(str(line).split("|"))
							else:
								quotes.append(str(line).split("|"))
					if quotes:
						quote = random.choice(quotes)
						txtout="```"+quote[1]+"```-"+quote[0]
					else:
						if len(message.content) > 7:
							txtout="No quotes found for `"+message.content[7:]+"`."
						else:
							txtout="Oops! No quotes available for this server!\nUse `"+prefix+"addquote <User>|<Quote>` to add quotes."
					print(txtout)
					await client.send_message(message.channel,txtout)
				except (IOError,IndexError):
					txtout="Oops! No quotes available for this server!\nUse `"+prefix+"addquote <User>|<Quote>` to add quotes."
					print("Broken Quote: "+str(quote))
					traceback.print_exc()
					await client.send_message(message.channel,txtout)
				f.close()   

			#@SOMEONE#
			elif settings["commands"]["@someone"]["command"] in message.content.lower().split(" ") and settings["commands"]["addquote"]["enabled"]==True:
				x = message.server.members
				members = []
				for member in x:
					if member.permissions_in(message.channel).read_messages and member.permissions_in(message.channel).send_messages:
						members.append(str(member.id))
				someone = random.choice(members)
				print(str(someone) + " was mentioned with @someone by " + str(message.author.id))
				txtout = "<@"+someone+">"+" was randomly mentioned with @someone!"
				await client.send_message(message.channel,txtout)

			#RETURN STRING WITH SPACES EVERY CHARACTER#
			elif message.content.lower().startswith(prefix+settings["commands"]["widespace"]["command"]) and settings["commands"]["widespace"]["enabled"]==True:
				txtout = ""
				for letter in message.content[10:]:
					txtout = str(txtout) + str(letter)
					txtout = str(txtout) + " "
				print(txtout)
				await client.send_message(message.channel,txtout)

			#VERBOSE MESSAGE GENERATOR#
			elif message.content.lower().startswith(prefix+settings["commands"]["verbose"]["command"]) and settings["commands"]["verbose"]["enabled"]==True:
				txtin = message.content[9:]
				txtout = ""
				synonyms = []
				for word in txtin.split():
					for syn in wordnet.synsets(word):
						for l in syn.lemmas():
							synonyms.append(l.name())
					if not synonyms:
							txtout+=(" " + word)
					else:
						txtout+=(" " + max(set(synonyms), key=len))
					synonyms = []
				txtout = txtout.replace("-"," ")
				txtout = txtout.replace("_"," ")
				print(txtout)
				await client.send_message(message.channel,txtout)

			#SUCCINCT MESSAGE GENERATOR#
			elif message.content.lower().startswith(prefix+settings["commands"]["succinct"]["command"]) and settings["commands"]["succinct"]["enabled"]==True:
				txtin = message.content[10:]
				txtout = ""
				synonyms = []
				for word in txtin.split():
					for syn in wordnet.synsets(word):
						for l in syn.lemmas():
							synonyms.append(l.name())
					if not synonyms:
						txtout+=(" " + word)
					else:
						txtout+=(" " + min(set(synonyms), key=len))
					synonyms = []
				txtout = txtout.replace("-"," ")
				txtout = txtout.replace("_"," ")
				print(txtout)
				await client.send_message(message.channel,txtout)

			#SMUSH TWO WORDS TOGETHER#
			elif message.content.lower().startswith(prefix+settings["commands"]["smush"]["command"]) and settings["commands"]["smush"]["enabled"]==True:
				worda = message.content.split(" ")[1]
				wordb = message.content.split(" ")[2]
				asyl = hyphenate_word(worda)
				bsyl = hyphenate_word(wordb)
				if len(bsyl) > 1:
					txtout = str(asyl[0]) + "".join(bsyl[1:])
				else: #in case word 2 is only 1 syllable, just join the words
					txtout = str(asyl[0]) + "".join(bsyl[0])
				txtout = worda+" "+wordb+" ("+txtout+")"
				print(txtout)
				await client.send_message(message.channel,txtout)

			elif message.content.lower().startswith(prefix+settings["commands"]["dog"]["command"]) and settings["commands"]["dog"]["enabled"]==True:
				with urllib.request.urlopen("https://dog.ceo/api/breeds/image/random") as url:
					data = json.loads(url.read().decode())
					embed = discord.Embed(color=0xeee657)
					embed.set_image(url=data["message"])
					print(data["message"])
					await client.send_message(message.channel,embed=embed)

			elif message.content.lower().startswith(prefix+settings["commands"]["catfact"]["command"]) and settings["commands"]["catfact"]["enabled"]==True:
				with urllib.request.urlopen("https://cat-fact.herokuapp.com/facts/random") as url:
					data = json.loads(url.read().decode())
					txtout=data["text"]
					print(txtout)
					await client.send_message(message.channel,txtout)

			#CHOOSE FROM USER SPECIFIED LIST#
			elif message.content.lower().startswith(prefix+settings["commands"]["choose"]["command"]) and settings["commands"]["choose"]["enabled"]==True:
				items=message.content[7:]
				txtout=random.choice(items.split("|"))
				print(txtout)
				await client.send_message(message.channel,txtout)

			#"RATE" SOMETHING BY PICKING A NUMBER FROM 1 TO 10#
			elif message.content.lower().startswith(prefix+settings["commands"]["rate"]["command"]) and settings["commands"]["rate"]["enabled"]==True:
				txtout="I\'d rate " + str(message.content[6:]) + " **" + str(random.randrange(10)) + " out of 10!**"
				print(txtout)
				await client.send_message(message.channel,txtout)

			#FLIP A COIN#
			elif message.content.lower().startswith(prefix+settings["commands"]["flip"]["command"]) and settings["commands"]["flip"]["enabled"]==True:
				embed = discord.Embed(title="Flip", description=random.choice(['Heads','Tails']), color=0xeee657)
				await client.send_message(message.channel, embed=embed)
			
			#PRINT EMOTES#
			elif message.content.lower().startswith(prefix+settings["commands"]["emotes"]["command"]) and settings["commands"]["emotes"]["enabled"]==True:
				txtout=""
				with open('emotes.txt','r') as file:
					lines=list(file)
				for x in range(int(message.content.lower().split(" ")[1])):
					txtout += str(random.choice(lines)).rstrip()
				print(message.content.lower().split(" ")[1]+" emojis")
				
				await client.send_message(message.channel,txtout)

			#PERFORM XKCD37#
			elif settings["commands"]["xkcd37"]["enabled"]==True and re.search(xkcd37,message.content):
				txtout = re.sub(xkcd37,xkcd37sub, message.content, 0)
				txtout = "```> "+txtout+"``` xkcd 37"
				print(txtout)
				await client.send_message(message.channel,txtout)

			#DADBOT#
			elif settings["commands"]["dadbot"]["enabled"]==True and (message.content.lower().split(" ")[0]=='i\'m' or message.content.lower().split(" ")[0]=='im'):
				txtout = "Hi " + " ".join(message.content.split(" ")[1:]) + ", I'm Dad"
				print(txtout)
				await client.send_message(message.channel,txtout)

			#REPLY TO COMMENTS ABOUT BOT#
			elif 'bot' in message.content.lower().split(" ") and settings["commands"]["bot"]["enabled"]==True:
				txtin = sid.polarity_scores(message.content)
				if float(txtin['compound']) >= 0.2:
					txtout=':heart:'
				elif float(txtin['compound']) <= 0.15 and float(txtin['compound']) >= -0.15:
					txtout='I am unfeeling'
				else:
					txtout='no u'
				print(txtout+' '+str(txtin['compound']))
				await client.send_message(message.channel,txtout)
			
			elif 'oopsie' in message.content.lower().split(" ") and settings["commands"]["oopsie"]["enabled"]==True:
				txtout="OOPSIE WOOPSIE!! Uwu We make a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this!"
				print(txtout)
				await client.send_message(message.channel,txtout)

			#GARBAGE MEME#
			elif settings["commands"]["peestream"]["command"] in message.content.lower() and settings["commands"]["peestream"]["enabled"]==True:
				embed = discord.Embed(color=0xeee657)
				embed.set_image(url="https://cdn.discordapp.com/attachments/260061122193784833/404628539728723969/chrome_2018-01-07_20-25-17.jpg")
				print("Pee Stream")
				await client.send_message(message.channel,embed=embed)
with open("bottoken_topsecret.txt","r") as bottoken:
	client.run(str(bottoken.read()))
client.close()