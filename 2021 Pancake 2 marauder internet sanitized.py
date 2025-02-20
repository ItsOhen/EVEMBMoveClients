#!/usr/bin/python

import win32gui
import win32api
import re
import time
import os
import json

eveo-location = "%UserProfile%\\Documents\\EVE-O\\"

# Clients to be stacked
Rats = [
	"Toon1",
	"Toon 2",
	"toon 3",
#	"_toon 4_"
]
# Clients to make a quad
Quads = [

]

# Clients with specific locations on the screen
# If added here, must include "EVE - " before the name
# X Y W H
Clients = {
	"EVE - SpecialToon1" : (0, 864, 1224, 864),
	"EVE - specialToon_2" : (1224, 864, 924, 864),
	"EVE - iLiveSomewhere on the screen" : (2148, 864, 924, 864),
#	"EVE - Notthisone" : (768, 864, 768, 864),
}

def AddClient(name, x, y, w, h):
    Clients["EVE - " + name] = [x,y,w,h]
    print(name + " added.")
	
def UpdateEVEO(fn, rats, x, height):
    with open(fn) as f:
        data = json.load(f)
    offset = (int)(height / len(rats))
    h = 0
    for client in rats:
        data['FlatLayout'][client] = "{0}, {1}".format(x,h)
        h += offset
    with open(fn, 'w') as json_file:
      json.dump(data, json_file)

def StackClients(clients, offset, width, height, maxwidth):
    count = len(clients)
    w = (int)((maxwidth - width) / (count - 1))
    x = offset
    ret = {}
    for client in Rats:
        AddClient(client, x, 0, width, height )
        x += w

def QuadClients(clients, offset, maxwidth, maxheight):
    width = (int)(maxwidth / 2)
    height = (int)(maxheight / 2)

    if len(clients) > 4 :
        print("Error! Can't excede 4 clients in quad mode stooopid!")
        return
    if len(clients) > 3 :
        AddClient(clients[3], offset+width,height,width,height)
    if len(clients) > 2 :
        AddClient(clients[2], offset,height,width,height)    
    if len(clients) > 1 :
        AddClient(clients[1], offset+width,0,width,height)
    if len(clients) > 0 :
        AddClient(clients[0], offset,0,width,height)
	
	
class WindowMgr:
	def __init__ (self):
		self._handle = []
	
	def find_window(self, class_name, window_name=None):
		self._handle = win32gui.FindWindow(class_name, window_name)
	
	def _window_enum_callback(self, hwnd, wildcard):
		if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
			self._handle.append(hwnd)
	
	def find_window_wildcard(self, wildcard):
		self._handle.clear()
		win32gui.EnumWindows(self._window_enum_callback, wildcard)
		
w = WindowMgr()
w.find_window_wildcard("EVE -*")
eveo = win32gui.FindWindow(0, "EVE-O Preview")
if eveo != 0:
	os.system('taskkill /f /im "EVE-O Preview.exe"')
counter = 0

#screen size = 3840x2160(4k) / 1.25(windows scale 125%) = 3072x1782
#offset is 0 for screen 0, 3072 for screen 1, 6144 for screen 2

#for stacked clients
#resolution = 1280x1080 (custom resolution in nvidia cpanel) / 1.25 = 1024x864 (1/3rd of 4k width, 1/2 height)

#for quad clients
#in-game resolution = 1920x1080 (1080P) / 1.25 = 1536x864

#QuadClients(Quads, 0, 3072, 864*2)
Rats.sort()
StackClients(Rats, 0, 1024,864, 1748)
UpdateEVEO(eveo-location + 'EVE-O Preview.json', Rats, 2180, 1080)

with open(eveo-location + 'EVE-O Preview.json') as f:
  data = json.load(f)

for handle in w._handle:
	name = win32gui.GetWindowText(handle)
#GetWindowText will grab the full EVE - {name} string so toss the EVE part
	if name in Clients:
		loc = Clients[name]
		win32gui.MoveWindow(handle, loc[0], loc[1], loc[2], loc[3], 1)
		win32api.SendMessage(handle, 0x232, 0, 0)
		counter += 1
		time.sleep(0.1)
time.sleep(0.1)
if counter > 6:
	try:
		win32api.WinExec(eveo-location + 'EVE-O Preview.exe')
	except:
		pass