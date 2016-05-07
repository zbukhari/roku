#!/usr/bin/python

# Programmer: Zahid Bukhari
# Purpose: Laziness
# Date: Forgot.
# Source URL: https://github.com/zbukhari/roku/

import urllib
import urllib2
import xml.etree.ElementTree as etree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("roku", help="Roku IP address")
args = parser.parse_args()
rokuServer = 'http://%s:8060' % args.roku

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

	apps = urllib2.urlopen('%s/query/apps' % rokuServer)
	
	tree = etree.parse(apps)
	root = tree.getroot()

	x = []
	for XMLOBJ in root.getchildren():
		x.append({'id':XMLOBJ.attrib['id'], 'type':XMLOBJ.attrib['type'], 'version':XMLOBJ.attrib['version'], 'value':XMLOBJ.text})

	apps.close()

	return x

def sendLitKeys(s):
	"""Function to send a string (s) to Roku"""

	print 'Sending %s' % s

	for y in range(len(s)):
		f = urllib2.urlopen('%s/keypress/Lit_%s' % (rokuServer, urllib.quote(s[y])), urllib.urlencode({'':''}))
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
	except ValueError, e:
		return False

	f = urllib2.urlopen('%s/keypress/%s' % (rokuServer, key), urllib.urlencode({'':''}))
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

	if d['command'] == 'launch':
		f = urllib2.urlopen('%s/launch/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'install':
		f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'query/apps':
		f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'keydown':
		f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'keyup':
		f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'keyDownUp':
		f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()
	elif d['command'] == 'query/icon':
		f = urllib2.urlopen('%s/install/%d' % (rokuServer, d['param']), urllib.urlencode({'':''}))
		z = f.read()
		f.close()

	return True

if __name__ == '__main__':
	while True:
		print """You want to primarily use the numeric keypad but it's your choice.

|-------|-------|-------|-------|
|       |   /   |   -   |   *   |       Other keys:
|       |       | Volume| INFO  |
|       | SEARCH| Down  |       |       Key => Action
|-------|-------|-------|-------|       ---------------------------------
|   7   |   8   |   9   |   +   |       S   => Send a string
|  <--  |   ^   |   @   | Volume|       l   => List applications
| BACK  |  UP   | HOME  | Up    |       L   => Launch application
|-------|-------|-------|       |       I   => Install application
|   4   |   5   |   6   |       |       q   => Quit
|   <   |   OK  |   >   |       |       _   => VolumeMute (underscore)
| LEFT  | SELECT| RIGHT |       |
|-------|-------|-------|-------|
|   1   |   2   |   3   |       |
|  <<   |   \/  |   >>  | Enter |
| REWIND| DOWN  | F-FWD |       |
|-------|-------|-------|   or  |
|       0       |   .   |       |
|     |> / ||   |  <<-  | Return|
|  PLAY / PAUSE | REPLAY|       |
|---------------|-------|-------|

Please enter a key: """

		c = getchar()

		if len(c) != 1:
			print 'Invalid number of characters and or invalid option'
			continue

		# Interface
		if c == '8':
			sendKeys2ECP('Up')
		elif c == '2':
			sendKeys2ECP('Down')
		elif c == '4':
			sendKeys2ECP('Left')
		elif c == '6':
			sendKeys2ECP('Right')
		elif c == '5':
			sendKeys2ECP('Select')
		elif c == '9':
			sendKeys2ECP('Home')
		elif c == '7':
			sendKeys2ECP('Back')
		elif c == '*':
			sendKeys2ECP('Info')
	
		# Playback
		elif c == '0':
			sendKeys2ECP('Play')
		elif c == '1':
			sendKeys2ECP('Rev')
		elif c == '3':
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
		elif c == 'S':
			s = raw_input('Enter string: ')
			sendLitKeys(s)
		elif c == 'l':
			apps = listApps()
			print map(lambda f: '%s %s' % (f['id'], f['value']), apps)
		elif c == 'L':
			appid = int(raw_input('Enter application ID: '))
			ecpSvcs(command='launch', param=appid)
		elif c == 'I':
			appid = int(raw_input('Enter application ID: '))
			ecpSvcs(command='install', param=appid)
		elif c == '*':
			sendKeys2ECP('Info')
		elif c == 'q' or c == 'Q':
			break
		else:
			print 'Invalid choice. Try again.'
