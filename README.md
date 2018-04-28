# bot
discord bot written in py

## Dependencies
---
* [hyphenate.py](https://nedbatchelder.com/code/modules/hyphenate.html "Ned Batchelder's Webpage") by Ned Batchelder (2007). Used for the `smush` command. 
* [discord.py](https://github.com/Rapptz/discord.py "python3 -m pip install -U discord.py") for discord integration, only text is required at this time. 
* [NLTK](https://github.com/nltk/nltk "pip install -U nltk") Used for the `verbose` and `succinct` commands. 
 * Wordnet
 * Vader

## Command List
---
Command | Syntax | Usage
---|---|---
`.addquote`|`.addquote <@user>|<quote>`|Adds a 'quote' to the server's quote.txt in `\quotes\`
`.quote`|`.quote [@user]`|Picks a random quote from the server's quote file. If a user is specified, returns the a random quote from that author.
`@someone`|any message containing `@someone`|Picks a random user from the server and mentions them. Ment to emulate discord's 2018 april fools joke. 
Dadbot|`I'm <message>`|Replies to user with the side splittingly hilarious 'Hi, \<so and so>, I'm Dad'. No, I will not remove this feature. 
`.widespace`|`.widespace <text>`|Inserts a space every second character of supplied text, for that `a e s t h e t i c` feeling.
`.verbose`|`.verbose <text>`|Attempts to sound smart by replaceing every word with a longer related word. Results may vary.
`.succinct`|`.succinct <text>`|The opposite of `.verbose`, picking the shortest related word. Less funny than `.verbose`.
`.smush`|`.smush <word1> <word2>`|Attempts to make a portmanteau of the two supplied words. Works best with long words.
`.choose`|`.choose <item1>|<item2>|<item3>|...`|Randomly picks one item out of a supplied array. 
`.rate`|`.rate <text>`|Randomly rates the supplied text out of 10.
`.flip`|`.flip`|Flip a coin, returns heads or tails.
`bot`|any message containing `bot`|Uses sentiment analysis to respond to comments about bot. Yes, it is overkill. 
