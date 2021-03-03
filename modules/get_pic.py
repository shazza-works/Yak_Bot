#!/user/bin/python3.8
#
#
# Get pic for stego command.
# Shazza-Works

import os
import sys
import requests


def getPic():
	url = "https://source.unsplash.com/random"
	r = requests.get(url)
	page = r.content
	f = open('steg/tmp.png', 'bw')
	f.write(page)
	f.close

###EOF###
