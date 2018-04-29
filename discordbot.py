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
from hyphenate import hyphenate_word
import nltk
from nltk.corpus import wordnet
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

@client.event
async def on_ready():
    print("Account: "+client.user.name)
    print("Account ID: "+client.user.id)
    print("Bot Account: "+str(client.user.bot))
    print("||||||||| ONLINE |||||||||")

@client.event
async def on_message(message):
    if not client.user.id == message.author.id:
        global txtout
        if message.content.lower().startswith(prefix+'test'):
            print(':robot:')
            await client.send_message(message.channel, ':robot:')
        
        elif message.content.lower().startswith(prefix+'info'):
            print('BOT INFO')
            embed = discord.Embed(title="BOT INFO", description="Made by @ShiftyWizard#4823 & @Arboreal#4200 for fun.", url="https://github.com/leaharboreal/bot", color=0x1abc9c)
            #embed.add_field(name="Github Repository", url="https://github.com/leaharboreal/bot")
            embed.set_thumbnail(url="https://raw.githubusercontent.com/leaharboreal/bot/master/profilepic.png")
            embed.set_footer(text="© bot", icon_url="https://raw.githubusercontent.com/leaharboreal/bot/master/profilepic.png")
            await client.send_message(message.channel, embed=embed)

        #ADD USER QUOTE TO FILE#
        elif message.content.lower().startswith(prefix+'addquote'):
            f = open(os.path.join('quotes',str(message.server.id+'.txt')),'a+')
            quotemessage = message.content[10:].split("|")
            f.write(quotemessage[0] + "|" + quotemessage[1]+'\n')
            print("Added Quote to file "+message.server.id+".txt: "+str(quotemessage))
            await client.send_message(message.channel,":white_check_mark:")
            f.close()
        #PICK RANDOM USER QUOTE#
        elif message.content.lower().startswith(prefix+'quote'):
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
            except (IOError,IndexError) as e:
                txtout="Oops! No quotes available for this server!\nUse `"+prefix+"addquote <User>|<Quote>` to add quotes."
                print("Broken Quote: "+str(quote))
                traceback.print_exc()
                await client.send_message(message.channel,txtout)
            f.close()   

        #@SOMEONE#
        elif '@someone' in message.content.lower().split(" "):
            x = message.server.members
            members = []
            for member in x:
                if member.permissions_in(message.channel).read_messages and member.permissions_in(message.channel).send_messages:
                    members.append(str(member.id))
            someone = random.choice(members)
            print(str(someone) + " was mentioned with @someone by " + str(message.author.id))
            txtout = "<@"+someone+">"+" was randomly mentioned with @someone!"
            await client.send_message(message.channel,txtout)

        #DADBOT#
        elif message.content.lower().startswith('i\'m') or message.content.lower().startswith('im'):
            txtout = "Hi " + " ".join(message.content.split(" ")[1:]) + ", I'm Dad"
            print(txtout)
            await client.send_message(message.channel,txtout)

        #RETURN STRING WITH SPACES EVERY CHARACTER#
        elif message.content.lower().startswith(prefix+'widespace'):
            txtout = ""
            for letter in message.content[10:]:
                txtout = str(txtout) + str(letter)
                txtout = str(txtout) + " "
            print(txtout)
            await client.send_message(message.channel,txtout)

        #VERBOSE MESSAGE GENERATOR#
        elif message.content.lower().startswith(prefix+"verbose"):
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
                    txtout+=(" " + max(set(synonyms), key=len))
                synonyms = []
            txtout = txtout.replace("-"," ")
            txtout = txtout.replace("_"," ")
            print(txtout)
            await client.send_message(message.channel,txtout)

        #SUCCINCT MESSAGE GENERATOR#
        elif message.content.lower().startswith(prefix+"succinct"):
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
        elif message.content.lower().startswith(prefix+"smush"):
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

        #CHOOSE FROM USER SPECIFIED LIST#
        elif message.content.lower().startswith(prefix+'choose'):
            items=message.content[7:]
            txtout=random.choice(items.split("|"))
            print(txtout)
            await client.send_message(message.channel,txtout)
        
        #"RATE" SOMETHING BY PICKING A NUMBER FROM 1 TO 10#
        elif message.content.lower().startswith(prefix+'rate'):
            txtout="I\'d rate " + str(message.content[6:]) + " **" + str(random.randrange(10)) + " out of 10!**"
            print(txtout)
            await client.send_message(message.channel,txtout)

        #FLIP A COIN#
        elif message.content.lower().startswith(prefix+'flip'):
            embed = discord.Embed(title="Flip", description=random.choice(['Heads','Tails']), color=0xeee657)
            await client.send_message(message.channel, embed=embed)

        #REPLY TO COMMENTS ABOUT BOT#
        elif 'bot' in message.content.lower().split(" "):
            txtin = sid.polarity_scores(message.content)
            if float(txtin['compound']) >= 0.2:
                txtout=':heart:'
            elif float(txtin['compound']) <= 0.15 and float(txtin['compound']) >= -0.15:
                txtout='I am unfeeling'
            else:
                txtout='no u'
            print(txtout+' '+str(txtin['compound']))
            await client.send_message(message.channel,txtout)

        #GARBAGE MEME#
        elif 'pee stream' in message.content:
            txtout = 'https://cdn.discordapp.com/attachments/260061122193784833/404628539728723969/chrome_2018-01-07_20-25-17.jpg'
            print(txtout)
            await client.send_message(message.channel,txtout)
with open("bottoken_topsecret.txt","r") as bottoken:
    client.run(str(bottoken.read()))
client.close()