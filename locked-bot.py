#!/usr/bin/python3
#
# Editors;
#        Azzassin, shazza-works, tomdoughty62
# Working Progress
#	  *___Need to catch this on startup___*
#	raise ClientConnectorError(req.connection_key, exc) from exc
#	NO NET ERROR
#
import discord
import os, sys, re
import json, time
import random, requests
import hashlib, base64
import hackernews
import subprocess, codecs
import asyncio
from random import choice
from googlesearch import search
from discord import Embed
from discord.ext import tasks
from modules import help
from modules import db_setup
from discord.ext import commands
from modules import mk_embed
from modules.mk_embed import colours as c
from modules import get_pic as gp
from discord.ext.commands import Bot
from modules.password_urls import urls # need this from @Toms new split pass and hash
from modules import databasescore as db_score


class tc:
    head = "\033[95m"
    blue = "\033[94m"
    cyan = "\033[96m"
    green = "\033[92m"
    yellow = "\033[93m"
    red = "\033[91m"
    nc = "\033[0m"
    bold = "\033[1m"
    underline = "\033[4m"

def check_steg():
    if subprocess.getoutput("command -v steghide") != '': #change to sys run and drop SP
        pass
    else:
        print (tc.yellow, "Warning !! (You need to install steghide in your terminal!)\n", tc.nc)
       	sys.exit(1)

check_steg()

try:
    tokenFile = open(sys.argv[1], "r")
    token = tokenFile.readline()
except IndexError:
    print (tc.red, "You need to give your token!\nUse; {} <token>".format(sys.argv[0]), tc.nc)
    exit(1)


print (tc.blue, "[?] WIPE--> HASH,SCORE,USER,WELCOME DB", tc.nc)
q = input("[yes or ENTER for NO]>")
if not q in ["y","Y", "yes", "Yes", "YES", "yer", "yerr", "ye", "yee", "yar", "yep"]:
    pass
else:
    db_setup.wipe_db()


bot = Bot(command_prefix="%", help_command=None)


@bot.event
async def on_help_command_error(ctx, error):
    print ("[!]ERROR;", error)
    c = commands.HelpCommand.send_error_message('Fuckyerr', error)
    await ctx.send(c.send())

@bot.event
async def on_ready():
    print (tc.green, f"[*] We have logged in as {bot.user.name} using ID {bot.user.id}", tc.nc)
    print (tc.green, f"[*] Discord.py Version: {discord.__version__}", tc.nc)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Squirrels Mate"))
    #await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with foof on the ham cutter ~"))
    print (tc.yellow, "[#] Status set as Listening and Online.", tc.nc) # we need to ask user on start ((DONE) see shazza)


@bot.event
async def on_message(message):
    users_welcomed = db_score.getUserWelcome()
    users = [x[0] for x in users_welcomed]
    if message.author.bot:
        return
    if not message.author.id in users:
        roles = discord.utils.get(message.guild.channels, name="roles")
        db_score.addUserWelcome(message.author.id)
        emb = discord.Embed(colour=0x111111, description=f"""Welcome to {message.author.guild} {message.author.mention},
            I am {bot.user.mention}, My command prefix is \' ~ \'
            Your in channel <#{message.channel.id}>
            Head over to <#{roles.id}> for a role
            Hope you enjoy your stay,
            Humans will be here soon...
            MSG> {message.content}""")
        await message.channel.send(embed=emb)
        await bot.process_commands(message)
    if message.channel.is_nsfw():
        safesearch = 'off'
    else:
        safesearch = 'on'
    for x in ['how to', 'how can i', 'how do i', 'what is', 'why is', 'where can i', 'why do', 'what would i']:
        pre, hit, after = message.content.lower().partition(x)
        if hit != '':
            srch = hit + after
            res = search(srch, lang='en', tbs='0', safe=safesearch, num=3, start=0, stop=3, verify_ssl=True)
            reso  = [ x for x in res ]
            urls = '\n'.join(reso)
            emb = mk_embed.emb(message, c.yellow, '',f"Here is some info on what you just asked...\n{urls}")
            await message.channel.send(embed=emb)
            await bot.process_commands(message)
        else:
            pass
    if bot.user.mentioned_in(message):
        emb = mk_embed.emb(message, c.yellow, '', f"Hi there I\'m {bot.user.name}, Use my prefix {bot.command_prefix}command to issue commands.")
        await message.channel.send(embed=emb)
        await bot.process_commands(message)
    if message.role_mentions:
        emb = mk_embed.emb(message, c.yellow, '',f"Hello there I\'m {bot.user.name}, If you need me try the command {bot.command_prefix}help for more info.")
        await message.channel.send(embed=emb)
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        try:
            await ctx.message.delete()
        except:
            pass
        print (tc.red, "[!] on_command_error: ", error, tc.nc)
        emb = mk_embed.emb(ctx, c.red, '', f"(⛔)𝙷𝚘𝚕𝚢 𝚄𝚗𝚍𝚎𝚛𝚌𝚛𝚊𝚌𝚔𝚎𝚛𝚜 𝙱𝚊𝚝𝚖𝚊𝚗,\n[{error}]\nCheck the command help ~help command_name")
        await ctx.send(embed=emb)
    if isinstance(error, commands.MissingPermissions):
        try:
            await ctx.message.delete()
        except:
            pass
        print (tc.red, "[!] on_command_error: ", error, tc.nc)
        emb = mk_embed.emb(ctx, c.red, '', "Missing Permissions")
        await ctx.send(embed=emb)

@commands.is_owner()
#@commands.has_permissions(administrator=True)
@bot.command(name="wipe", help="Wipe a user from the db {admin_only}", description="Wipe a users data and welcome from the DB")
async def wipe(ctx, user):
    try:
        await ctx.message.delete()
    except:
        pass
    db_score.purgeUser(re.sub("\D", '', user)) #this regex needs fixing (try 2x ids !)
    db_score.purgeScore(re.sub("\D", '', user))
    emb = mk_embed.emb(ctx, c.red, '', f"User data for {user} deteted.")
    await ctx.send(embed=emb)

@wipe.error
async def wipe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)



@bot.command(name="test", description="Tools;", help="Use to test bot sone string here")
async def test(ctx, *args):
    try:
        await ctx.message.delete()
    except:
        pass
    print (tc.yellow, f"[*] Test was called by {ctx.author}", tc.nc)
    user_args = ", ".join(args)
    emb = mk_embed.emb(ctx, c.black, '', f"Hello {ctx.author}, you sent {user_args}")
    await ctx.send(embed=emb)
    return

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

### HELP ###
@bot.command(name="help")
async def help_cmd(ctx, cmd=''):
    try:
        await ctx.message.delete()
    except:
        pass
    cmds = ["add","b32","b64","calc","dm_me","hasher","joke","make","pool","ranks","rot13","score","status","stego","submit","test","wipe","xgif","news","search","fancy","prefix","delpool","quiz"]
    if not cmd in cmds:
        emb = mk_embed.emb(ctx, c.blue, '', help.main_help)
        await ctx.send(embed=emb)
    else:
        msg = eval("help."+cmd)
        emb = mk_embed.emb(ctx, c.blue, '', msg)
        await ctx.send(embed=emb)

used = []
@bot.command(name="hasher", description="Games;", help="Make a hash to crack for points.")
async def hasher(ctx, args):
    try:
        await ctx.message.delete()
    except:
        pass
    def get_page(urls):
        url = random.choice(urls)
        page = requests.get(url)
        while page.status_code != 200:
            print (tc.red, "[*] URL returned non-200 code, trying another...", tc.nc)
            page = get_page(urls)
        page = page.text.split("\n")
        return page

    page = get_page(urls)

    if args == "easy":
        for t in page:
            if (len(t) <= 8) and t not in used:
                word = t
                base64_digest = codecs.encode(t.encode("utf-8"), "base64").decode().strip()
                md5_digest = hashlib.md5(t.encode("utf-8")).hexdigest()
                sha1_digest = hashlib.sha1(t.encode("utf-8")).hexdigest()
                hash_array = random.choice([md5_digest, sha1_digest, base64_digest])
                db_score.addHash(word, hash_array, 150)
                print (tc.yellow, "[!]Hasher-used", t, "<--->", hash_array, tc.nc)
                used.append(word)
                break
            else:
                pass
        else:
            get_page(urls)
    elif args == "medium":
        for t in page:
            if (len(t) > 8) and (len(t) <= 10) and t not in used:
                word = t
                _digest = hashlib.md5(t.encode("utf-8")).hexdigest()
                md5_digest = hashlib.md5(t.encode("utf-8")).hexdigest()
                sha1_digest = hashlib.sha1(t.encode("utf-8")).hexdigest()
                sha3_224_digest = hashlib.sha3_224(t.encode("utf-8")).hexdigest()
                hash_array = random.choice([md5_digest, sha1_digest, sha3_224_digest])
                db_score.addHash(word, hash_array, 250)
                print (tc.yellow, "[!]Hasher-used", t, "<--->", hash_array, tc.nc)
                used.append(word)
                break
            else:
                pass
        else:
            get_page(urls)
    elif args == "hard":
        for t in page:
            if (len(t) > 10) and t not in used:
                word = t
                sha256_digest = hashlib.sha256(t.encode("utf-8")).hexdigest()
                sha512_digest = hashlib.sha512(t.encode("utf-8")).hexdigest()
                sha3_384_digest = hashlib.sha3_384(t.encode("utf-8")).hexdigest()
                sha384_digest = hashlib.sha384(t.encode("utf-8")).hexdigest()
                blake2b_digest = hashlib.blake2b(t.encode("utf-8")).hexdigest()
                hash_array = random.choice([sha256_digest, sha512_digest, sha384_digest, sha3_384_digest, blake2b_digest])
                db_score.addHash(word, hash_array, 350)
                print (tc.yellow, "[!]Hasher-used", t, "<--->", hash_array, tc.nc)
                used.append(word)
                break
            else:
                pass
        else:
            get_page(urls)
    else:
        emb = mk_embed.emb(ctx, c.red, '', "That iss not a set option use [easy, medium, hard]")
        await ctx.send(embed=emb)
    emb = mk_embed.emb(ctx, c.yellow, '', f"Your hash is; {hash_array}")
    await ctx.send(embed=emb)

@hasher.error
async def hasher_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That iss not a set option use [easy, medium, hard]")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)


@bot.command(name="stego", description="Games;", help="Make a picture with a hidden message for you to crack.")
async def stego(ctx):   #### ADD SOME POINTS TO THIS AS WELL ####
    try:
        await ctx.message.delete()
    except:
        pass
    gp.getPic()
    # @Tom put your random DB password and hash get here.
    FLAG = "@Tom needs to set MSG + DB HASH HERE for well done you made it.\n"
    text = "steg/flag.txt"
    pic = "steg/tmp.png"
    newpic = "steg/steg.jpg"
    password = random.choice(["password", "FooFoo","Flipflop","flappyPoo","FreAkin44","frodoPool1","Test_M3","Try-pass-here","easy1"])
    cmd = [f"steghide --embed -f -cf {pic} -ef {text} -sf {newpic} -p {password}"] # fstring
    if os.path.exists(text):
        pass
    else:
        f = open(text, "w")
        f.write(FLAG)
        f.close()
    print (tc.green, "[*] Log; " + subprocess.getoutput(cmd), tc.nc)
    print (tc.green, f"[*] Log; {ctx.author} called stego command using password = {password}", tc.nc)
    await ctx.send(file=discord.File(newpic), content="Hey, {0} Your stego file is here...".format(ctx.author.mention))


@bot.command(name="joke", description="Tools;", help="Gives you a random joke.")
async def joke(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    URL = "https://official-joke-api.appspot.com/random_joke"
    randomize = random.choice(c.randomize)
    r = requests.get(URL)
    if r.status_code == 200:
        setup = r.json()["setup"]
        punchline = r.json()["punchline"]
        emb = mk_embed.emb(ctx, randomize, '', f"Q; {setup}\nA; {punchline}\n")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "Error getting your joke!\n", tc.nc)
        exit(1)


@bot.command(name="dm_me", description="Tools;", help="What it sounds like, Send yourself a DM.")
async def dm_me(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    dmToUser = await ctx.author.create_dm()
    await dmToUser.send("Hello there")
	#can we make it respond back?


@bot.command(name="make", description="Tools;", help="Create an account to keep the points you gain in games.")
async def make(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    username = ctx.author
    userid = ctx.author.id
    score = db_score.addUser(userid)
    accmadeday = db_score.getAccDate(userid)[0]
    print (tc.green, f"[*] {ctx.author.name} requested to make an account...", tc.nc)
    if score[0]:
        emb = mk_embed.emb(ctx, c.blue, '', "Your account has been created! :D")
        await ctx.send(embed=emb)
        print (tc.green, f"[*] The account was added! User ID {username}", tc.nc)
    else:
        emb = mk_embed.emb(ctx, c.blue, '', f"You have got an account,\nyou made it on {accmadeday}")
        await ctx.send(embed=emb)


@bot.command(name="score", description="Games;", help="Check your Guild account score.")
async def score(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    userid = ctx.author.id
    score = db_score.checkUserScore(userid)[0]
    if score == None:
        emb = mk_embed.emb(ctx, c.red, '', "You need to make an account first, using the make command")
        await ctx.send(embed=emb)
    else:
        emb = mk_embed.emb(ctx, c.blue, '', f"Your account currently has {score} points.")
        await ctx.send(embed=emb)

@score.error
async def score_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        emb = mk_embed.emb(ctx, c.red, '', "You need to make an account first silly billy !")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)


@bot.command(name="rot13", description="Tools;", help="Encode / Decode ROT13.")
async def rot13(ctx, *, arg):
    try:
        await ctx.message.delete()
    except:
        pass
    key = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz "
    char = "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm "
    out = []
    rot13 = dict(zip(key, char))
    for x in arg:
        if x not in key:
            pass
        else:
            out.append(rot13[x])
    emb = mk_embed.emb(ctx, c.black, "ROT_13", ''.join(out))
    await ctx.send(embed=emb)

@rot13.error
async def rot13_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)


@bot.command(name="b64", description="Tools;", help="b64 [ -e encode ][ -d decode ][ MSG ]")
async def b64(ctx, setting, *, message):
    try:
        await ctx.message.delete()
    except:
        pass
    if message == '':
        emb = mk_embed.emb(ctx, c.red, '', "You need to give me a message..")
        await ctx.send(embed=emb)
        return
    if setting == "-d":
        msg = codecs.decode(message.encode(), "base64").decode().strip()
        emb = mk_embed.emb(ctx, c.black, '', msg)
        await ctx.send(embed=emb)
    elif setting == "-e":
        msg = codecs.encode(message.encode(), "base64").decode().strip()
        emb = mk_embed.emb(ctx, c.black, '', msg)
        await ctx.send(embed=emb)

@b64.error
async def b64_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "You need to use ~b64  -e [encode] msg OR -d [decode] msg")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## b32
@bot.command(name="b32", description="Tools;", help="b32 [ -e encode ][ -d decode ][ MSG ]")
async def b32(ctx, setting, *, message):
    try:
        await ctx.message.delete()
    except:
        pass
    if message == '':
        emb = mk_embed.emb(ctx, c.red, '', "You need to give me a message..")
        await ctx.send(embed=emb)
        return
    if setting == "-d":
        msg = base64.b32decode(message.encode("utf-8")).decode().strip()
        emb = mk_embed.emb(ctx, c.black, '', msg)
        await ctx.send(embed=emb)
    elif setting == "-e":
        msg = base64.b32encode(message.encode("utf-8")).decode().strip()
        emb = mk_embed.emb(ctx, c.black, '', msg)
        await ctx.send(embed=emb)

@b32.error
async def b32_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "You need to use ~b32  -e [encode] msg OR -d [decode] msg")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## submit
@bot.command(name="submit", description="Games;", help="Submit your task to get points..")
async def submit(ctx, password, hash):
    try:
        await ctx.message.delete()
    except:
        pass
    userExists = db_score.checkUserScore(ctx.author.id)
    if userExists == None:
        emb = mk_embed.emb(ctx, c.blue, '', "Doese not look like you have an account, making one now...")
        await ctx.send(embed=emb)
        db_score.addUser(ctx.author.id)
    points = db_score.checkHash(password, hash)
    if points == 0:
        emb = mk_embed.emb(ctx, c.red, '', "Sorry, that dose not look right, or it is already been cracked.")
        await ctx.send(embed=emb)
        return
    db_score.addPoints(ctx.author.id, points)
    emb = mk_embed.emb(ctx, "00ff00", '', f"Well done {ctx.author.mention}, you have earned {points} points! :D")
    await ctx.send(embed=emb)

@submit.error
async def submit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly (Try help command)")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## pool
@bot.command(name="pool", description="Tools;", help="See if any hash are un-cracked")
async def getpool(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    request = db_score.getPool()
    if request == []:
        emb = mk_embed.emb(ctx, c.blue, '', "All hashes have been cracked,\nmake more with ~hasher [level]")
        await ctx.send(embed=emb)
    else:
        out = []
        request = db_score.getPool()
        out.append("\_PTS_\t\t\t\t\t\t\t\_\_HASH\_\_")
        for x in request:
            out.append(''.join("+"+str(x[0])+"\t<{}>\t"+x[1]))
        emb = mk_embed.emb(ctx, c.yellow, '', "These hash still need cracking for points,\n____See if you can snag them____\n\n{0}".format("\n".join(out)))
        await ctx.send(embed=emb)

@getpool.error
async def getpool_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## ranks
@bot.command(name="ranks", help="Print User Scoreboard")
async def ranks(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    data = db_score.callScoreBoard()
    out = []
    for i in data:
        a,b = i[0], i[1]
        if (a != None) :
            try :
                user = await bot.fetch_user(a)
                username = user.name
            except :
                continue
                #The code raises an error if it can't find the user
        else :
            continue
            #The code crashes if we send a null value to the api, this is to prevent that
        out.append(f"ID> {username}, PTS>{b},\n")
    msg = ''.join(out)
    emb = mk_embed.emb(ctx, c.green, '', msg)
    await ctx.send(embed=emb)

@ranks.error
async def ranks_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## add
@commands.is_owner()
#@commands.has_permissions(administrator=True)
@bot.command(name="add", help="Bulk add users to db {admin_only}", description="Used by admin to add accounts")
async def adduser(ctx, *, args):
    try:
        await ctx.message.delete()
    except:
        pass
    for x in args.split():
        userid = re.sub("\D", '', x)
        score = db_score.addUser(userid)
        if score[0]:
            emb = mk_embed.emb(ctx, c.green, '', f"Added <@{userid}>\'s account to db.")
            await ctx.send(embed=emb)
            print (tc.green, f"[*] User account added with ID {userid}", tc.nc)
        else:
            accmadeday = db_score.getAccDate(userid)
            emb = mk_embed.emb(ctx, c.blue, '', f"<@{userid}> You\'ve got an account,\nyou made it on {accmadeday[0]}")
            await ctx.send(embed=emb)

@adduser.error
async def adduser_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## calculator
@bot.command(name="calc", help="Calculator for Discord....(Im simple).", aliases=["cal", "ca", "c"])
async def calc(ctx, x: int, px: str, y: int):
    try:
        await ctx.message.delete()
    except:
        pass
    if px == "+":
        ans = x + y
        emb = mk_embed.emb(ctx, c.yellow, '', f"Sum of x and y is {ans}")
        await ctx.send(embed=emb)
    if px == "-":
        ans = x - y
        emb = mk_embed.emb(ctx, c.yellow, '', f"Difference of x and y is {ans}")
        await ctx.send(embed=emb)
    if px == "/":
        ans = x / y
        emb = mk_embed.emb(ctx, c.yellow, '', f"Quotient of x and y is {ans}")
        await ctx.send(embed=emb)
    if px == "*":
        ans = x * y
        emb = mk_embed.emb(ctx, c.yellow, '', f"Product of x and y is {ans}")
        await ctx.send(embed=emb)
    if px == "//":
        ans = x // y
        emb = mk_embed.emb(ctx, c.yellow, '', f"Quotient from floor division of x and y is {ans}")
        await ctx.send(embed=emb)
    if px == "%":
        ans = x % y
        emb = mk_embed.emb(ctx, c.yellow, '', f"Remainder of x / y is {ans}")
        await ctx.send(embed=emb)
    if px == "**":
        ans = x ** y
        emb = mk_embed.emb(ctx, c.yellow, '', f"x to the y power is {ans}")
        await ctx.send(embed=emb)


@calc.error
async def calc_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb = mk_embed.emb(ctx, c.red, '', "That is not how you use it silly ( Try; ~help command_name )")
        await ctx.send(embed=emb)
    else:
        print (tc.red, "[!]ERROR;", error, tc.nc)

## status
@commands.is_owner()
#@commands.has_permissions(administrator=True)
@bot.command(name='status')
async def status(ctx, user_status, *, user_info: str):
    try:
        await ctx.message.delete()
    except:
        pass
    opts = [ 'online','offline','idle','dnd','invisible']
    if user_status in opts:
        status = discord.Status(user_status)
        activity = discord.Game(name=user_info)
        emb = mk_embed.emb(ctx, c.yellow, '', f"Setting status to {user_status}")
        await ctx.send(embed=emb)
        await bot.change_presence(status=status, activity=activity)
        print (f'[#] Status set as {status}')
        emb = mk_embed.emb(ctx, c.green, '', "Status Set.")
        await ctx.send(embed=emb)
    else:
        emb = mk_embed.emb(ctx, c.blue, '', "That is not an option try [online,offline,idle,dnd,invisible]")
        await ctx.send(embed=emb)

@status.error
async def status_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        print (tc.red, "[!] ERROR: ", error, tc.nc)
        emb = mk_embed.emb(ctx, c.red, '', "Forbidden: 403 Bot Missing Permissions To Set Status...!")
        await ctx.send(embed=emb)

## news
pull = hackernews.hn.NewsClient()
newsID = pull.get_new_story_ids()
@bot.command(name='news')
async def tech_news(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    def new_post():
            post = random.choice(newsID)
            data = pull.get_item_by_id(post)
            return data
    data = new_post()
    while data.url == None:
            data = new_post()
    else:
            title = data.title
            footer = data.text
            url = data.url
    embed = discord.Embed(title="{}".format(title), description="{}".format(url), url="{}".format(url))
    r = requests.get(url).text
    icon  = re.findall('"((http)?s://.*?(jpg|png))"', r)[:1]
    if footer != None:
            embed.set_footer(text="{}".format(footer))
            embed.set_image(url=''.format(icon))
            await ctx.send(embed=embed)
    else:
            await ctx.send(url)


@commands.is_nsfw()
@bot.command(name="xgif")
async def pbot(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    out = []
    while len(out) <= 100:
        url = "https://cdn.boob.bot/Gifs/"
        x = random.choice(['A','B','C','D','E','F'])
        y = random.choice(['0','1','2','3','4','5','6','7','8','9'])
        z = random.choice(['16', '17', '18'])
        i = url+str(z)+str(y)+x+'.gif'
        r = requests.get(i)
        if r.reason != "OK":
             pass
        else:
             out.append(url+str(z)+str(y)+x+'.gif')
        while len(out) != 0:
            await ctx.send(out.pop())
            break
        break

@pbot.error
async def wipe_error(ctx, error):
    if isinstance(error, commands.NSFWChannelRequired):
        print ("[!] Not an  NSFW: ", error)
        emb = mk_embed.emb(ctx, c.red, '', "This is not an NSFW chan now is it !!")
        await ctx.send(embed=emb)


@commands.is_owner()
#@commands.has_permissions(administrator=True)
@bot.command(name="prefix")
async def prefix(ctx, prefix):
    try:
        await ctx.message.delete()
    except:
        pass
    bot.command_prefix = prefix
    emb = mk_embed.emb(ctx, c.blue, '', f"Prefix changed to {prefix}")
    await ctx.send(embed=emb)


@bot.command(name="search")
async def search_google(ctx, *, args: str):
    try:
        await ctx.message.delete()
    except:
        pass
    res = search(args, tld='com', lang='en', tbs='0', safe='on', num=3, start=0, stop=3, verify_ssl=True)
    reso  = [ x for x in res ]
    urls = '\n'.join(reso)
    emb = mk_embed.emb(ctx, c.yellow, '', f"Your search is here...\n{urls}")
    await ctx.send(embed=emb)


@bot.command(name="fancy")
async def txt(ctx, *, args):
    try:
        await ctx.message.delete()
    except:
        pass
    s = "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ\ .⓪①②③④⑤⑥⑦⑧⑨"
    t = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\ .0123456789'
    randomize = random.choice(c.randomize)
    lst = dict(zip(t, s))
    out = []
    for x in args:
        try:
            out.append(lst[x])
        except KeyError:
            pass
    msg = ''.join(out)
    emb = mk_embed.emb(ctx, randomize, '', f"{msg}")
    await ctx.send(embed=emb)


@bot.command(name='delpool')
async def delpool(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    db_score.wipePool()
    emb = mk_embed.emb(ctx, c.blue, '', "All Hash Pool Data Now Cleared Form DB.")
    await ctx.send(embed=emb)


@bot.command(name='quiz')
async def quiz(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
    ctx = ctx
    def check(msg):
        return msg.author == ctx.author

    TOPICS_LIST = ['science', 'history', 'commerce', 'technology', 'worldgk']

    async def ask_one_question(question, key):
        randomize = random.choice(c.randomize)
        emb = mk_embed.emb(ctx, randomize, '', f"{key}) {question}\nEnter Your Choice \[a/b/c/d/exit]:")
        await ctx.send(embed=emb)
        message = await bot.wait_for('message', timeout=30, check=check)
        ch = message.content.lower()
        while(True):
            if ch in ['a', 'b', 'c', 'd']:
                return ch
            if ch == "exit":
                return 'exit'
            else:
                emb = mk_embed.emb(ctx, c.red, '', "Invalid choice. Enter again \[a,b,c,d]")
                await ctx.send(embed=emb)
                message = await bot.wait_for('message', timeout=30, check=check)
                choice = message.content
                return choice

    async def score_one_result(key, meta):
        actual = meta["answer"]
        if meta["user_response"].lower() == actual.lower():
            return 0, f"Q.{key}Correct 💪 Nice!"
        else:
            return -1, f"Q.{key}Wrong, Answer is ({actual}) 👎"

    async def test(questions):
        score = 10
        emb = mk_embed.emb(ctx, c.yellow, '', "General Instructions 💡\n1.Please enter only the choice letter corresponding to the correct answer.\n2. Each question carries 1 points.\n3. Wrong answer leads to -1 marks per question.\nQuiz will start momentarily.\nGood Luck 👍\n")
        await ctx.send(embed=emb)
        time.sleep(10)
        for key, meta in questions.items():
            questions[key]["user_response"] = await ask_one_question(meta["question"], key)
            if questions[key]["user_response"] == 'exit':
                emb = mk_embed.emb(ctx, c.red, '', "You asked to quit see you next time 🚀")
                await ctx.send(embed=emb)
                return
        results = []
        for key, meta in questions.items():
            num, info = await score_one_result(key, meta)
            score += int(num)
            results.append(info)
        test = score / len(questions) * 100
        lst = '\n'.join(results)
        ans = f"🔥🔥🔥🔥🔥RESULT🔥🔥🔥🔥🔥\n\n{lst}\n\nYour Score: {score} / {(len(questions))} -- {test}%"
        emb = mk_embed.emb(ctx, c.green, '', ans)
        await ctx.send(embed=emb)

    async def load_question(filename):
        try:
            os.remove('topics/ask.json')
        except FileNotFoundError:
            pass
        out = []
        with open(filename, "r") as r:
            in_data = json.load(r)
            w = open('topics/ask.json', 'a')
            keys = list(in_data.keys())
            json_data = {}
            info = {}
            for x in range(1,11):
                n = choice(keys)
                while n in out:
                    n = choice(keys)
                out.append(n)
                info = in_data[str(n)]
                json_data[str(x)] = info
        w.write(json.dumps(json_data, indent=4))
        w.close()
        questions = None
        with open('topics/ask.json', "r") as read_file:
            questions = json.load(read_file)
        return (questions)

    async def play_quiz():
        flag = False
        try:
            emb = mk_embed.emb(ctx, c.yellow, '', "Welcome to Today's Quiz 🐧!\nChoose your domain of interest ❓:\n(1). Science ⚗️\n(2). History of India 🕌\n(3). Commerce 💵\n(4). Technology 📠\n(5). General Knowledge 🙈\nEnter Your Choice [1/2/3/4/5]:")
            await ctx.send(embed=emb)
            message = await bot.wait_for('message', timeout=30, check=check)
            choice = int(message.content)
            if choice > len(TOPICS_LIST) or choice < 1:
                emb = mk_embed.emb(ctx, c.red, '', "Invalid Choice. Enter Again ❗")
                await ctx.send(embed=emb)
                flag = True # raising flag
        except ValueError as e:
            emb = mk_embed.emb(ctx, c.red, '', "Invalid Choice. Enter Again ❗")
            await ctx.send(embed=emb)
            flag = True # raising a flag
        if not flag:
            questions = await load_question('topics/'+TOPICS_LIST[choice-1]+'.json')
            await test(questions)
        else:
            await play_quiz() # replay if flag was raised

    async def user_begin_prompt():
        emb = mk_embed.emb(ctx, c.yellow, '', "Wanna test your General Knowledge ❓\nA. Yes\nB. No")
        await ctx.send(embed=emb)
        message = await bot.wait_for('message', timeout=30, check=check)
        play = message.content
        if play.lower() == 'a' or play.lower() ==  'y':
            await play_quiz()
        elif play.lower() == 'b':
            emb = mk_embed.emb(ctx, c.black, '', "Hope you come back soon ❓")
            await ctx.send(embed=emb)
        else:
            emb = mk_embed.emb(ctx, c.red, '', "Hmm. I didn't quite understand that.\nPress A to play, or B to quit ❗")
            await ctx.send(embed=emb)
            await user_begin_prompt()

    try:
        await user_begin_prompt()
    except asyncio.TimeoutError: # timeout error handling
        emb = mk_embed.emb(ctx, c.red, '', "You took TOO long, See Ya Next Time...❗")
        await ctx.send(embed=emb)

try:
    bot.run(token)
except:
    print ("You Don't Have A Network Dummy !!")
