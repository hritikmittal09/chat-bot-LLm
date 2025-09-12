import json
import os 
files = { "Spotify" : r"C:\Users\Lenovo\AppData\Roaming\Spotify\Spotify.exe" }
 
def getShortcutsList():
 return list(files.keys())

def openFile(fileName):
 if fileName == '':
  return
 else :
  os.system(files[fileName])
  return
