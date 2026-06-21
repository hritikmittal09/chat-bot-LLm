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


def openFile(fileName: str):

    fileName = fileName.lower().strip()

    path = files.get(fileName)

    if not path:
        return f"{fileName} shortcut not found"

    if path.startswith("http"):
        webbrowser.open(path)
        return f"Opened website: {path}"

    else:
        os.startfile(path)
        return f"Opened application: {path}"

def file_options():
   loadFilesPaths()
   global files
   filesoptioms = list(files.keys())
   return " ,".join(filesoptioms)
if __name__ == "__main__":
   print(file_options())






