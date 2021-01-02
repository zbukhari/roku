#!/usr/bin/python3

# Programmer: Zahid Bukhari
# Purpose: Laziness
# Date: Forgot.
# Source URL: https://github.com/zbukhari/roku/

import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as etree
import argparse
import ssdp
import re

parser = argparse.ArgumentParser()
parser.add_argument("roku", help="Roku IP address", nargs='?', default=False)
args = parser.parse_args()

if args.roku:
	rokuServer = 'http://{}:8060'.format(args.roku)
else:
	rokuList = ssdp.discover('roku:ecp')

	rokuListLen = len(rokuList)

	if rokuListLen == 1:
		rokuServer = rokuList[0].location
	else:
		for i in range(rokuListLen):
			deviceInfo = urllib.request.urlopen('{}query/device-info'.format(rokuList[i].location))
			tree = etree.parse(deviceInfo)
			root = tree.getroot()
			XMLOBJ = root.getchildren()

			rokuInfoDict = dict(list(zip([f.tag for f in XMLOBJ], [f.text for f in XMLOBJ])))
			rokuInfoDict['location'] = rokuList[i].location
			rokuInfoDict['usn'] = rokuList[i].usn

			if type(rokuInfoDict['friendly-device-name']) != None:
				print(('{0}. {1} (i.e. {2} {3}), Location: {4}'.format(
					i+1,
					rokuInfoDict['friendly-device-name'],
					rokuInfoDict['model-name'],
					rokuInfoDict['model-number'],
					rokuList[i].location)))
			else:
				print(('{0}. {1} {2}, Location: {3}'.format(
					i+1,
					rokuInfoDict['model-name'],
					rokuInfoDict['model-number'],
					rokuList[i].location)))

		# Choose here
		j = int(input('Enter in the number of the Roku device to connect to: '))

		if j < 1 or j > len(rokuList) + 1:
			print(('Incorrect number chosen : {}'.format(j)))
			exit(2)
		else:
			rokuServer = rokuList[j - 1].location

# getchar taken from https://gist.github.com/jasonrdsouza/1901709
def getchar():
	#Returns a single character from standard input
	import tty, termios, sys
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)

	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return ch

def listApps():
	"""Function to return applications from Roku as a Python data object (dictionary)"""

	apps = urllib.request.urlopen('{}query/apps'.format(rokuServer))

	tree = etree.parse(apps)
	root = tree.getroot()

	x = []
	for XMLOBJ in root.getchildren():
		x.append({'id':XMLOBJ.attrib['id'], 'type':XMLOBJ.attrib['type'], 'version':XMLOBJ.attrib['version'], 'value':XMLOBJ.text})

	apps.close()

	return x

def sendLitKeys(s):
	"""Function to send a string (s) to Roku"""

	print(('Sending {}'.format(s)))

	for y in range(len(s)):
		f = urllib.request.urlopen('{}keypress/Lit_{}'.format(rokuServer, urllib.parse.quote(s[y])), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()

	return

def sendKeys2ECP(key):
	"""Function to send various other types of keys to Roku

Valid Roku keys are: Home, Rev, Fwd, Play, Select, Up, Down, Left, Right, Down,
  Back, InstantReplay, Info, Backspace, Search, and Enter."""

	options = ('Home', 'Rev', 'Fwd', 'Play', 'Select', 'Left', 'Right', 'Down',
		'Up', 'Back', 'InstantReplay', 'Info', 'Backspace', 'Search',
		'Enter', 'VolumeDown', 'VolumeMute', 'VolumeUp')

	try:
		x = options.index(key)
	except(ValueError, e):
		return False

	f = urllib.request.urlopen('{}keypress/{}'.format(rokuServer, key), urllib.parse.urlencode({'':''}).encode('utf-8'))
	z = f.read()
	f.close()

	return True

def ecpSvcs(**d):
	"""Function to perform External Control Protocol Services

query/apps
keydown
keyup
keyDownUp
keypress
launch
install
query/icon
input"""

	# I have no idea what I was puffing here but they all say install
	if d['command'] == 'launch':
		f = urllib.request.urlopen('{}launch/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'install':
		f = urllib.request.urlopen('{}install/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'query/apps':
		f = urllib.request.urlopen('{}install/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'keydown':
		# f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		f = urllib.request.urlopen('{}install/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'keyup':
		# f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		f = urllib.request.urlopen('{}install/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'keyDownUp':
		# f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		f = urllib.request.urlopen('{}install/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'query/icon':
		# f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		f = urllib.request.urlopen('{}install/{}'.format(rokuServer, d['param']), urllib.parse.urlencode({'':''}))
		z = f.read()
		f.close()

	return True

if __name__ == '__main__':
	while True:
		print(("""Connected to {}

    101/104/105 key friendly            Alternate laptop friendly
|-------|-------|-------|-------|   |-------|-------|-------|-------|
|       |   /   |   -   |   *   |   |       |   /   |   -   |   *   |   Other keys:
|       |       | Volume| INFO  |   |       |       | Volume| INFO  |
|       | SEARCH| Down  |       |   |       | SEARCH| Down  |       |   Key => Action
|-------|-------|-------|-------|   |-------|-------|-------|-------|   ---------------------------------
|   7   |   8   |   9   |   +   |   |  r/R  |  t/T  |  y/Y  |   +   |  s/S  => Send a string
|  <--  |   ^   |   @   | Volume|   |  <--  |   ^   |   @   | Volume|   l   => List applications
| BACK  |  UP   | HOME  | Up    |   | BACK  |  UP   | HOME  | Up    |   L   => Launch application
|-------|-------|-------|       |   |-------|-------|-------|       |  i/I  => Install application
|   4   |   5   |   6   |       |   |  f/F  |  g/G  |  h/H  |       |  q/Q  => Quit
|   <   |   OK  |   >   |       |   |   <   |   OK  |   >   |       |   _   => VolumeMute (underscore)
| LEFT  | SELECT| RIGHT |       |   | LEFT  | SELECT| RIGHT |       |
|-------|-------|-------|-------|   |-------|-------|-------|-------|
|   1   |   2   |   3   |       |   |  v/V  |  b/B  |  n/N  |       |
|  <<   |   \/  |   >>  | Enter |   |  <<   |   \/  |   >>  | Enter |
| REWIND| DOWN  | F-FWD |       |   | REWIND| DOWN  | F-FWD |       |
|-------|-------|-------|   or  |   |-------|-------|-------|   or  |
|       0       |   .   |       |   |    [SPACE]    |   .   |       |
|     |> / ||   |  <<-  | Return|   |     |> / ||   |  <<-  | Return|
|  PLAY / PAUSE | REPLAY|       |   |  PLAY / PAUSE | REPLAY|       |
|---------------|-------|-------|   |---------------|-------|-------|

Please enter a key: """.format(rokuServer)))

		c = getchar()

		if len(c) != 1:
			print('Invalid number of characters and or invalid option')
			continue

		# Interface
		if c in ['8','t','T']:
			sendKeys2ECP('Up')
		elif c in ['2','b','B']:
			sendKeys2ECP('Down')
		elif c in ['4','f','F']:
			sendKeys2ECP('Left')
		elif c in ['6','h','H']:
			sendKeys2ECP('Right')
		elif c in ['5','g','G']:
			sendKeys2ECP('Select')
		elif c in ['9','y','Y']:
			sendKeys2ECP('Home')
		elif c in ['7','r','R']:
			sendKeys2ECP('Back')
		elif c == '*':
			sendKeys2ECP('Info')
	
		# Playback
		elif c in ['0',' ']:
			sendKeys2ECP('Play')
		elif c in ['1','v','V']:
			sendKeys2ECP('Rev')
		elif c in ['3','n','N']:
			sendKeys2ECP('Fwd')
		elif c == '.':
			sendKeys2ECP('InstantReplay')
		elif c == '+':
			sendKeys2ECP('VolumeUp')
		elif c == '-':
			sendKeys2ECP('VolumeDown')
		elif c == '_':
			sendKeys2ECP('VolumeMute')
	
		# Other keys
		elif c == '':
			sendKeys2ECP('Enter')
		elif c == '/':
			sendKeys2ECP('Search')
		elif c in ['s','S']:
			s = input('Enter string: ')
			sendLitKeys(s)
		elif c == 'l':
			apps = listApps()
			for l in ['{} {}'.format(f['id'], f['value']) for f in apps]:
				print(l)
		elif c == 'L':
			appid = int(input('Enter application ID: '))
			ecpSvcs(command='launch', param=appid)
		elif c in ['i','I']:
			appid = int(input('Enter application ID: '))
			ecpSvcs(command='install', param=appid)
		elif c == '*':
			sendKeys2ECP('Info')
		elif c in ['q','Q']:
			break
		else:
			print('Invalid choice. Try again.')
