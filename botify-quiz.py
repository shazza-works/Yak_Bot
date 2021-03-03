#!/usr/bin/python3
import discord, os, re
import sys, json, time
from random import choice
import subprocess, asyncio
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext import tasks

try:
    tokenFile = open(sys.argv[1], "r")
    token = tokenFile.readline()
except IndexError:
    print ("You need to give your token!\nUse; {} <token>".format(sys.argv[0]))
    exit(1)

bot = Bot(command_prefix=discord.ext.commands.when_mentioned_or("%"))

@bot.event
async def on_ready():
	print ('We have logged in as BOT Smith')

@bot.command(name='quiz')
async def quiz(ctx):
    ctx = ctx
    def check(msg):
        return msg.author == ctx.author
    await ctx.send("Starting...")

    TOPICS_LIST = ['science', 'history', 'commerce', 'technology', 'worldgk']

    async def ask_one_question(question, key):
        await ctx.send(f"{key}) {question}\nEnter Your Choice \[a/b/c/d/exit]:")
        message = await bot.wait_for('message', timeout=30, check=check)
        ch = message.content.lower()
        while(True):
            if ch in ['a', 'b', 'c', 'd']:
                return ch
            if ch == "exit":
            	return 'exit'
            else:
                await ctx.send("Invalid choice. Enter again \[a,b,c,d]")
                message = await bot.wait_for('message', timeout=30, check=check)
                choice = message.content

    async def score_one_result(key, meta):
        actual = meta["answer"]
        if meta["user_response"].lower() == actual.lower():
            return 0, f"Q.{key}Correct 💪 Nice!"
        else:
            return -1, f"Q.{key}Wrong, Answer is ({actual}) 👎"

    async def test(questions):
        score = 10
        await ctx.send("General Instructions 💡\n1.Please enter only the choice letter corresponding to the correct answer.\n2. Each question carries 1 points.\n3. Wrong answer leads to -1 marks per question.\nQuiz will start momentarily.\nGood Luck 👍\n")
        time.sleep(10)
        for key, meta in questions.items():
            questions[key]["user_response"] = await ask_one_question(meta["question"], key)
            if questions[key]["user_response"] == 'exit':
                await ctx.send("You asked to quit see you next time 🚀")
                return
        await ctx.send("\n🔥🔥🔥🔥🔥🔥RESULT🔥🔥🔥🔥🔥🔥\n")
       	results = []
        for key, meta in questions.items():
            num, info = await score_one_result(key, meta)
            score += int(num)
            results.append(info)
        await ctx.send("\n".join(results))
        test = score / len(questions) * 100
        await ctx.send(f"Your Score: {score} / {(len(questions))} -- {test}%")

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
            await ctx.send("Welcome to Today's Quiz 🐧!\nChoose your domain of interest ❓:\n(1). Science ⚗️\n(2). History of India 🕌\n(3). Commerce 💵\n(4). Technology 📠\n(5). General Knowledge 🙈\nEnter Your Choice [1/2/3/4/5]:")
            message = await bot.wait_for('message', timeout=30, check=check)
            choice = int(message.content)
            if choice > len(TOPICS_LIST) or choice < 1:
                await ctx.send("Invalid Choice. Enter Again ❗")
                flag = True # raising flag
        except ValueError as e:
            await ctx.send("Invalid Choice. Enter Again ❗")
            flag = True # raising a flag
        if not flag:
            questions = await load_question('topics/'+TOPICS_LIST[choice-1]+'.json')
            await test(questions)
        else:
            await play_quiz() # replay if flag was raised

    async def user_begin_prompt():
        await ctx.send("Wanna test your General Knowledge ❓\nA. Yes\nB. No")
        message = await bot.wait_for('message', timeout=30, check=check)
        play = message.content
        if play.lower() == 'a' or play.lower() ==  'y':
            await play_quiz()
        elif play.lower() == 'b':
            await ctx.send("Hope you come back soon ❓")
        else:
            await ctx.send("Hmm. I didn't quite understand that.\nPress A to play, or B to quit ❗")
            await user_begin_prompt()

    try:
        await user_begin_prompt()
    except asyncio.TimeoutError: # timeout error handling
        await ctx.send("You took TOO long, See Ya Next Time...❗")

try:
    bot.run(token)
except:
    print ("You Don't Have A Network Dummy !!")
