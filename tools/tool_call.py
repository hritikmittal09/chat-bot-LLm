from tools.weather import get_weather
from tools.websearch import web_search
from File_Explore import openFile

def run_get_weather(args):
    return get_weather(args["city"])

def run_web_search(args):
    return web_search(args["q"])

def open_File(args):
    fileName = args["fileName"]
    return openFile(fileName)


tool_map = {
    "get_weather": run_get_weather,
    "web_search":  run_web_search,
    "open_file" : open_File 
}