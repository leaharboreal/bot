#!/usr/bin/env python3
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
	await client.change_presence(game=discord.Game(name="Use .info for help."))

	#Lists local server files that have no corresponding server
	for file in os.listdir('settings'):
		if not os.path.basename(file)[0] in client.Servers:
			print(client.user.name + " has been removed from " + os.path.basename(file) + ", or the server no longer exists. ")
			print("To remove this warning, remove the file from the servers directory. ")
	print("||||||||| READY |||||||||")
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

			elif message.content.lower().startswith(prefix+settings["commands"]["settings"]["command"]) and message.author.server_permissions.manage_server:
				#upgrade the file's read permissions to rw#
				serversettings.close()
				with open(os.path.join('settings',str(message.server.id+'.json')),'r+') as serversettings:
					#convert the current server's settings.json file into a python object#
					settings = json.loads(serversettings.read())
					
					#set changed to false so if no setting is modified the file will be unchanged#
					changed=False
					
					#check if number of args in message is high enough else reply with syntax error#
					if len(message.content.lower().split(" "))>1:
						
						#check if the first argument is commands#
						if message.content.lower().split(" ")[1]=="commands":
							
							#check if number of args in message is high enough for this branch#
							if len(message.content.lower().split(" "))>2:
								
								#ensure the command exists and is not the info or settings command#
								if (message.content.lower().split(" ")[2] in settings["commands"]) and not (message.content.lower().split(" ")[2] in ["info","settings"]):
									
									#check if number of args in message is high enough for this branch#
									if len(message.content.lower().split(" "))>3 and len(message.content.lower().split(" "))<6:
										
										#check if the user wants to change the command alias#
										if message.content.lower().split(" ")[3]=="command":
											
											#ensure the command contains only safe characters and is smaller or equal to 16 characters#
											if re.match(r"^[\w\d~!@#$%^&+=;:,./?\*\-]{1,16}$",message.content.lower().split(" ")[4]):
												
												#set the selected command to the alias#
												settings["commands"][message.content.lower().split(" ")[2]]["command"]=message.content.lower().split(" ")[4]
												
												#set changed to true, ensuring the file is saved#
												changed=True
												
												#set output message to confirmation#
												txtout = message.content.lower().split(" ")[2]+" has been set to "+message.content.lower().split(" ")[4]
											
											#reject command alias#
											else:
												txtout = "Could not set command. Commands can only 1-16 characters long and contain letters, numbers and these symbols: `~!@#$%^&+=;:,./?*-`"
										
										#check if the user wants to change if command is enabled#
										elif message.content.lower().split(" ")[3]=="enabled":
											
											#check if argument is true#
											if message.content.lower().split(" ")[4]=="true":
												
												#set the commands enabled value to true#
												settings["commands"][message.content.lower().split(" ")[2]]["enabled"]=True
												
												#set changed to true, ensuring the file is saved#
												changed=True
												
												#set output message to confirmation#
												txtout = message.content.lower().split(" ")[2]+" is now `enabled`."
											
											#check if answer is false if not true#
											elif message.content.lower().split(" ")[4]=="false":
												
												#set the commands enabled value to false#
												settings["commands"][str(message.content.lower().split(" ")[2])]["enabled"]=False
												
												#set changed to true, ensuring the file is saved#
												changed=True
												
												#set output message to confirmation#
												txtout = message.content.lower().split(" ")[2]+" is now `disabled`."
											
											#reject value as it is not true or false#
											else:
												txtout = "This value can only be set to `true` or `false`."
										#unrecognised argument#
										else:
											txtout = "Incorrect syntax(E:2). `"+prefix+"settings commands "+message.content.split(" ")[2]+" <command|enabled> <value>`"
									#not enough args#
									else:
										txtout = "Incorrect syntax (E:1). `"+prefix+"settings commands "+message.content.split(" ")[2]+" <command|enabled> <value>`"
								#unrecognised/locked argument#
								else:
									txtout = "Command `"+message.content.split(" ")[2]+"` not found or cannot be modified. Check the github page command list which can be accessed with `"+prefix+"info`"
							#not enough args#
							else:
								txtout = "Incorrect syntax. `"+prefix+"settings commands <commandname> <command|enabled> <value>`"
						
						#check if the first argument is bot, if it isn't commands#		
						elif message.content.lower().split(" ")[1]=="bot":
							
							#check if number of args in message is high enough for this branch#
							if len(message.content.lower().split(" "))>2:
								
								#check if arg is equal to prefix#
								if message.content.lower().split(" ")[2]=="prefix":
									
									#check if number of args in message is high enough for this branch#
									if len(message.content.lower().split(" "))>3:
										
										#check if user's value matches rule#
										if re.match(r"^[\w\d~!@#$%^&+=;:,./?\*\-]{1,4}$",message.content.split(" ")[3]):
											
											#set bot prefix to the user value#
											settings["bot"]["prefix"]=message.content.lower().split(" ")[3]
											
											#set changed to true, ensuring the file is saved#
											changed=True
											
											#set output message to confirmation#
											txtout = "Prefix set. Bot will respond to commands with the prefix `"+message.content.lower().split(" ")[3]+"`. To access settings, use the new prefix."
										
										#reject prefix as it does not conform to the character requirements#
										else:
											txtout = "Could not set prefix. Prefixes can only 1-4 characters long and contain letters, numbers and these symbols: `~!@#$%^&+=;:,./?*-`"
									
									#not enough args#
									else:
										txtout = "Incorrect syntax. `"+prefix+"settings bot prefix <value>`"
								
								#incorrect arg#
								else:
									txtout = "Incorrect syntax. `"+prefix+"settings bot prefix <value>`"
							
							#not enough args#
							else:
								txtout = "Incorrect syntax. `"+prefix+"settings bot prefix <value>`"
						
						#the first argument is incorrect, so respond with a syntax error#
						else:
							txtout = "Incorrect syntax. `"+prefix+"settings <commands|bot>`"
					
					#not enough args#
					else:
						txtout = "Incorrect syntax. `"+prefix+"settings <commands|bot>`"
					
					#if the file has been changed at any point, save changes#
					if changed:
						serversettings.seek(0)# reset file position to the beginning.
						json.dump(settings, serversettings, indent=4)
						serversettings.truncate()
					
					#log output in console then send as discord message#
					print(txtout)
					await client.send_message(message.channel,txtout)

			#.addquote#
			elif message.content.lower().startswith(prefix+settings["commands"]["addquote"]["command"]) and settings["commands"]["addquote"]["enabled"]==True:
				
				#check if the quotes file exists for the server, if not, create a file with an empty json object#
				if not os.path.isfile(os.path.join('quotes',str(message.server.id+'.json'))):
					with open(os.path.join('quotes',str(message.server.id+'.json')), 'a') as f:
						f.write("{\n}") 
				#open the server's quote file#
				with open(os.path.join('quotes',str(message.server.id+'.json')),'r+') as f:
					quotes = json.loads(f.read()) #initialize json file as python object#
					
					#set quotemessage to the message object before the user's command#
					async for message in client.logs_from(message.channel,limit=1,before=message.timestamp,reverse=False):
						quotemessage = message
					
					#ensure quote does not contain any illegal symbols#
					if re.match(r"^[\w\d~!@#$%^&+=;:, ./?\*\-]+$",quotemessage.content.lower()):
						if quotemessage.author.id in quotes: #if the user already has a quote object then append quote#
							quoteid = int(max(quotes[quotemessage.author.id].keys()))+1
							quotes[str(quotemessage.author.id)][quoteid] = str(quotemessage.content)
						else: #if they don't have a quote object, create one with their 1st quote#
							quoteid = 1
							quotes[quotemessage.author.id]={}
							quotes[quotemessage.author.id][quoteid] = str(quotemessage.content)
						
						print("Added Quote to file "+message.server.id+".json: "+str(quotemessage.content)) #add log of changes#
						await client.send_message(message.channel,":white_check_mark: Added quote: `"+str(quotemessage.content)+"`") #confirm addition of quote#
						
						#seek to start of file before dumping the new json object in the file#
						f.seek(0)
						json.dump(quotes, f, indent=4)
						f.close() #close the file since we are done with it#
					else: #tell user that the quote contains invalid characters#
						await client.send_message(message.channel,":negative_squared_cross_mark: Quote contains invalid characters.")
						f.close() #close the file since we are done with it#
			
			#.quote#
			elif message.content.lower().startswith(prefix+settings["commands"]["quote"]["command"]) and settings["commands"]["quote"]["enabled"]==True:
				if os.path.isfile(os.path.join('quotes',str(message.server.id+'.json'))):
					with open(os.path.join('quotes',str(message.server.id+'.json')),'r') as f:
						quotes = json.loads(f.read())
						if len(message.content.split(" "))>=2:
							if str(re.match(r".+(\d{18}).+",message.content).group(1)) in quotes.keys():
								quoteauthor = str(re.match(r".+(\d{18}).+",message.content).group(1))
								txtout="```"+str(quotes[quoteauthor][random.choice(list(quotes[quoteauthor].keys()))])+"``` -<@!"+str(quoteauthor)+">"
							else:
								txtout="Oops! "+message.content.split(" ")[1]+" hasn't been quoted on this server yet.\nUse `"+prefix+"addquote` when they say something great."
						else:
							quoteauthor = random.choice(list(quotes.keys()))
							txtout="```"+str(quotes[quoteauthor][random.choice(list(quotes[quoteauthor].keys()))])+"``` -<@!"+str(quoteauthor)+">"
				else:
					txtout="Oops! No quotes available for this server!\nUse `"+prefix+"addquote` to add quotes."
				print(txtout)
				await client.send_message(message.channel,txtout)

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
				x = ""
				for char in message.content[len(prefix+settings["commands"]["widespace"]["command"]):]:
					if ord(char) in range(33,127):
						x = chr(ord(char)+0xFEE0)
					else:
						x = char
					txtout = txtout + str(x) + " "
				print(txtout)
				await client.send_message(message.channel,txtout)

			#VERBOSE MESSAGE GENERATOR#
			elif message.content.lower().startswith(prefix+settings["commands"]["verbose"]["command"]) and settings["commands"]["verbose"]["enabled"]==True:
				txtin = message.content[len(prefix+settings["commands"]["verbose"]["command"]):]
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
				txtin = message.content[len(prefix+settings["commands"]["succinct"]["command"]):]
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
				items=message.content[len(prefix+settings["commands"]["choose"]["command"]):]
				txtout=random.choice(items.split("|"))
				print(txtout)
				await client.send_message(message.channel,txtout)

			#"RATE" SOMETHING BY PICKING A NUMBER FROM 1 TO 10#
			elif message.content.lower().startswith(prefix+settings["commands"]["rate"]["command"]) and settings["commands"]["rate"]["enabled"]==True:
				txtout="I\'d rate " + str(message.content[len(prefix+settings["commands"]["rate"]["command"]):]) + " **" + str(random.randrange(10)) + " out of 10!**"
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