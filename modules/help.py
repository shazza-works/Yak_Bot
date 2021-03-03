main_help = """
\t\t\t\t__***COMMANDS***__
\t*-add-*  __*** Add to db {admin}***__
\t*-b32-*  __*** Base32 Codec***__
\t*-b64-*  __*** Base64 Codec***__
\t*-calc-*  __*** Simple Calc ***__
\t*-dm_me-*  __*** DM Yourself***__
\t*-hasher-*  __*** Make a Hash***__
\t*-help-*  __*** Show this help***__
\t*-joke-*  __*** Random Joke.***__
\t*-make-*  __*** Create an account***__
\t*-pool-*  __*** List un-cracked Hash***__
\t*-ranks-*  __*** Full Scoreboard***__
\t*-rot13-*  __*** ROT13 Codec***__
\t*-score-*  __*** Your Score.***__
\t*-stat-*  __*** Bot Status {admin}***__
\t*-stego-*  __*** Make a Stego to Crack.***__
\t*-submit-*  __*** Submit your Crack***__
\t*-test-*  __*** Post Test***__
\t*-wipe-*  __*** Wipe a user {admin}***__
\t*-news-*  __*** Random Tech News***__
\t*-xgif-*  __*** Tiz Da Naughty {NSFW_ONLY}***__
\t*-search-*  __*** Look for web search***__
\t*-prefix-*  __*** Set the bots prefix {admin}***__
\t*-fancy-*  __*** Try our best to fancy msg***__
\t*-delpool-*  __*** Spring clean the db pool***__
\t*-quiz-*  __*** Test your skills in topic select***__

Type ~help command for more info on a command.
"""
add = """
Usage; add [@UserTag2200]

This command is used to add more users to the db or in bulk if needed for testing and dev work. (admin).
"""
b32 = """
Usage; b32 encode -e, decode -d [msg to use]

Base32 encoder and decoder, use this with the -e encode or -d decode flag and your message.
"""

b64 = """
Usage; b64 encode -e, decode -d [msg to use]

Base64 encoder and decoder, use this with the -e encode or -d decode flag and your message.
"""

calc = """
Usage; calc [X] %  +  //  -  /  *  [Y]

Simple calculator that can use the set above do do simple calculations example X + Y.
"""

dm_me = """
Usage; dm_me

Send yourself a dm from the bot, will add more features to this at some point.
"""

hasher = """
Usage; hasher [easy,medium,hard]

This command can be used with the chosen level as your argument and will create a hash to cracked for points on the hack bot games. If needed you can find crack tools online!
"""

joke = """
Usage; joke

Nice and easy api to give you a random joke, if you don't like one... hit it again.
"""

make = """
Usage; make

Used to make yourself a profile on the db. No info is needed and your data is just points and id. Show date made if exist.
"""

pool = """
Usage; pool

Show the pool of created but un-cracked hashers in the db, they will be left over from other users and can be stolen and cracked for the points shown.
"""

ranks = """
Usage; ranks

Display all users with an account in a scoreboard style print out, ready for a good I'm #1 roasting!
"""

rot13 = """
Usage; rot13 [MSG]

Rot13 is so common for CTF it had to go on the list of tools. Usage is very much like the base tools except there is no need to select mode as it will be auto. Just give it a message.
"""

score = """
Usage; score

Prints out your score on it's own so if you want to keep track of it and not print the whole socoreboare you can.
"""

status = """
Usage; status [online,offline,ndn,invisible] [MSG]

Handy way to set the status of the bot in chat, this will have more features added soon for stat and playing message but for now it's just stat. (admin)
"""

stego = """
Usage; stego

Stego will make you a random pic with steganography embed in the immage that you will have to crack in order to submit for points if you can ?

More Info;
https://www.2daygeek.com/easy-way-hide-information-inside-image-and-sound-objects/
"""

submit = """
Usage; submit [PASSWORD] [HASH]

Nice and easy here, submit the task you just did for your points. Use the command name and then the plain text password a space and then the hash, and for stego just the hash.
"""

test = """
Usage; test [MSG]

This handy tool will check the bot's respondimg and reply to your msg with a standard greeting and your message back.
"""

wipe = """
Usage; wipe [@UserTag2200]

Wipe a users data from the db, this will not only remove the user ID and points but also the welcome log too. As if the user is new to the guild (admin).
"""

news = """
Usage; news

Will give you a random tech related post for you to enjoy.
"""

xgif = """
Usage; xgif

This is an NSFW channel only command but if you have the role and your in a dirty channel crack on!
"""

search = """
Usage; search [MSG]

Get inf from a Google.com search in safe mode on any message you type after the command.
"""

prefix = """
Usage; prefix [PREFIX]

This is a dev tool to se the bots command prefix and is again an admin only tool.
"""

fancy = """
Usage; fancy [MSG]

Try and convert all the msg text to fancy text, if some is missing it cant convert it.
"""

delpool = """
Usage; delpool

This is a new command to clean out the un-cracked hash pool, for now it can be used by any user. If people start messing with it tho i will make it admin only!
"""

quiz = """
Usage; quiz

This easy to use quiz will test your skills and you may find it rather hard on some questiins, give it a try and see how you do!
"""
