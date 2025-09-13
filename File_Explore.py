import json
import webbrowser
import os 
files = dict()



def loadFilesPaths():
   try:
     with open("filepaths.json") as f :
      global files
      files = json.load(f)
      return
   except Exception as e :
      print("Unble to load file paths")
 
def getShortcutsList():
 loadFilesPaths()
 return list(files.keys())
def openFile(fileName :str):
    if fileName == '':
        return
    elif files[fileName].startswith('http') :
       webbrowser.open(files[fileName])
       print("i am here !")
       return
    else :
        
        os.startfile( files[fileName])
        return
