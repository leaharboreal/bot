# bot
discord bot written in py
![alt text](https://raw.githubusercontent.com/leaharboreal/bot/master/banner.png "banner")

## Setup
### Host bot yourself
1. Install Python 3
2. Install all [dependencies](https://github.com/leaharboreal/bot#dependencies).
[Hyphenate.py](https://nedbatchelder.com/code/modules/hyphenate.html "Ned Batchelder's Webpage") should be placed in the root directory (The directory containing `discordbot.py`)
3. Create the quotes directory in the root directory (`\quotes\`). This is where your quotes will be placed.
5. If you haven't already, create an application [on this page](https://discordapp.com/developers/applications/me "Discord Developer")
4. Create a text file only containing your private discord bot token. This file must be encoded in **UTF-8**, and named `bottoken_topsecret.txt`. This file should **not** be publicly available.
6. Invite your bot to a server with your OAuth link that can be generated on the discord website.

### Invite bot to your server
To invite bot to a server that you manage, click [here](https://discordapp.com/oauth2/authorize?client_id=426669660549677056&scope=bot "Invite bot") and follow the prompts. Bot is a project just for fun, and therefor may not be running 24/7. The bot may be taken down at any time without warning. If you have a problem with this you can host bot yourself using the instructions above. I'm not a lawyer or anything but _**please don't**_ misuse bot for anything:  
a) illegal  
b) objectionable/questionable  

## Dependencies
---
* [hyphenate.py](https://nedbatchelder.com/code/modules/hyphenate.html "Ned Batchelder's Webpage") by Ned Batchelder (2007). Used for the `smush` command. Should be located in the root folder (The directory with `discordbot.py`)
* [discord.py](https://github.com/Rapptz/discord.py "python3 -m pip install -U discord.py") for discord integration, only text is required at this time. 
* [NLTK](https://github.com/nltk/nltk "pip install -U nltk") Used for the `verbose` and `succinct` commands. 
 * Wordnet
 * Vader

## Command List
---
Command | Syntax | Usage
---|---|---
`.test`|`.test`|Test if bot can see and reply to commands. Replies with "🤖" (`:robot:`).
`.settings`|`.settings <bot> prefix <value>` or `.settings <commands> <command> <command\|enabled> <value>`|Sets command settings server wide. Must have minimum of server manager privlages to use. 
`.addquote`|`.addquote <@user>\|<quote>`|Adds a 'quote' to the server's quote.txt in `\quotes\`
`.quote`|`.quote [@user]`|Picks a random quote from the server's quote file. If a user is specified, returns the a random quote from that author.
`@someone`|any message containing `@someone`|Picks a random user from the server and mentions them. Meant to emulate discord's 2018 april fools joke. 
Dadbot|`I'm <message>`|Replies to user with the side splittingly hilarious 'Hi, \<so and so>, I'm Dad'. No, I will not remove this feature. 
Auto XKCD-37|any message containing `something-ass something`|Automatically performs https://xkcd.com/37/ on all messages. E.g. `sweet-ass car` becomes `sweet ass-car`
`.widespace`|`.widespace <text>`|Inserts a space every second character of supplied text, for that `a e s t h e t i c` feeling.
`.verbose`|`.verbose <text>`|Attempts to sound smart by replacing every word with a longer related word. Results may vary.
`.succinct`|`.succinct <text>`|The opposite of `.verbose`, picking the shortest related word. Less funny than `.verbose`.
`.smush`|`.smush <word1> <word2>`|Attempts to make a portmanteau of the two supplied words. Works best with long words.
`.choose`|`.choose <item1>\|<item2>\|<item3>\|...`|Randomly picks one item out of a supplied array. 
`.rate`|`.rate <text>`|Randomly rates the supplied text out of 10.
`.flip`|`.flip`|Flip a coin, returns heads or tails.
`.dog`|`.dog`|Returns a random dog image using the dog.ceo api.
`.catfact`|`.catfact`|Returns a random cat fact using a catfacts api.
`bot`|any message containing `bot`|Uses sentiment analysis to respond to comments about bot. Yes, it is overkill. 

## Contact
Something isn't working? Contact [@ShiftyWizard#4823 or @arboreal#4200](http://discord.gg/YKbEgNp "Click to join Arboreal's Discord Server") on discord. 