#!/data/data/com.termux/files/usr/bin/python3
import sys
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot
import get_pic as gp

try:
	tokenFile = open(sys.argv[1], "r")
	token = tokenFile.readline()
except IndexError:
	print ("You need to give your token!\nUse; ["+sys.argv[0]+" <token>]")
	exit(1)

bot = Bot(command_prefix='~')

@bot.event
async def on_ready():
	try:
		print ('We have logged in as {}'.format(bot.user.name))
		print (bot.user.id)
		print ('Discord.py Version: {}'.format(discord.__version__))
	except Exception as e:
		print("Ohh Shit Error = " + e)


@bot.command(name='foof')
async def foof(ctx):
	gp.getPic()
	await ctx.send(file=discord.File('tmp.png'), content='Here Is Your Pic From Local')

@bot.event
async def on_command_error(ctx, error):
	print ("[!] on_command_error: ", error)
	await ctx.send("⟮⛔⟯ 𝐻𝑜𝑙𝑦 𝑢𝑛𝑑𝑒𝑟𝑐𝑟𝑎𝑐𝑘𝑒𝑟𝑠 𝐵𝑎𝑡𝑚𝑎𝑛,\n𝑆𝒉𝑖𝑡'𝑠 𝐵𝑟𝑜𝑘𝑒𝑛.. [{}]".format(error))

bot.run(token)

###EOF###
