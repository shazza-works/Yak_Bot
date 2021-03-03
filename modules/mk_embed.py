#!/usr/bin/python3.8
#
# Small function to make a msg an embed
# Shazza_Works
#
# [ syntax = COLOUR, AUTHOR, TITLE, "DESCRIPTION" "COLOUR" ]
#
#  main text 3 as 1 and 1 as 3
#
############################################################

import discord
from discord import Embed

class colours:
	# easy pick colours
	red = 'ff0000'
	green = '00ff00'
	yellow = 'ffff00'
	blue = '00ffff'
	white = 'ffffff'
	pink = 'ff00ff'
	black = '111111'
	army = 'badd11'

	# shazza-works randome colour if needed for embed or other function.
	randomize = [
		'135EAB','13679E','13C1B3','13C3EF','148CFC','1560B5','16C273','1770B1','17845D','17A1F2','19484F','19F145',
		'1AB691','1CDF2E','1CFB85','1D55D9','1DBDDB','1EABB4','1FE369','227D55','23C94D','23DC4A','23F094','24CA20',
		'26E33F','271684','277C4E','2818EB','286174','28DDC4','2A73CD','2A7DB2','2D6E9E','2E737E','301937','301EEA',
		'311AEC','31974F','31D724','359953','378D3D','37D85F','37E8D4','37EF41','387BF4','3BF797','3C8423','3CE0D5',
		'3D7468','3D9491','423363','42B62B','444ADF','44BF37','44EBF0','4530CE','464256','464CC1','47A4BD','494754',
		'4B35BD','4BA3FB','4D5C71','4EBDFB','502D7B','514423','51D770','52BE67','538F15','5594CA','568A15','56CF2A',
		'58AC3A','5965E8','5BA2CC','5BD32F','5C87C0','5CC0F7','5CCD22','5E8EB7','5FE1CD','6030B4','60836C','61F19A',
		'64C718','662B71','66A05D','66D0D4','672129','67BE55','67E645','67FA7C','6A13C6','6A71C9','6C71C8','6CDC6E',
		'6D6259','6E1683','72EC87','73E77E','75CD23','76BFF8','76C68F','77A09A','785696','788D61','78B018','79A887',
		'7D2561','8027FC','83FB98','84D0F9','8587CB','85CB3D','861578','877864','88D150','891A8E','8B6EA1','8C94BC',
		'8EE5B7','9291E4','93DA20','94C3ED','9650C9','983D45','99F810','9CE4BD','9EDAE3','9F266E','9FED34','A2C9A5',
		'A2CAC0','A3EB89','A53873','A58B31','A6F34C','A7C77B','A828B1','AB2872','ABF0AE','AC4CA0','AD1E3D','AD30D3',
		'AD5C30','ADD5CB','AF1F1D','B020CE','B07B6A','B1A8EF','B1DBE3','B257A6','B26258','B2DD6A','B3EE8C','B42523',
		'B494F6','B49A8E','B68475','B6D95F','B6E53D','B76B23','B86738','BC1EF1','C31672','C73CAB','C7B068','C7CBDD',
		'C81F8B','C9A34A','C9ECA6','CDE588','CF14F4','D05FE6','D08A54','D18055','D52A15','D9555F','DC1DE5','DCDD8F',
		'DEE9FC','E133B9','E1C4CB','E21641','E2BD5C','E46171','E5852D','E5968C','E61523','E68492','E84454','EA9AD9',
		'ECA239','EF7EED','EFD9E1','F04E86','F1EADF','F2522C','F2A636','F31DAB','F3F336','F68445','F74821','F8F659',
		'F9252D','F97A1B','F9FB82','FABDF4'
		]



def emb(ctx, colour='0x111111', title="", description=""):
	emb = discord.Embed(colour=int(colour, base=16), title=title, description=description) # 1+2
	emb = emb.set_author(name=ctx.author.name) # 3 Info Title or User etc
	emb = emb.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png?size=1024")
	return emb
