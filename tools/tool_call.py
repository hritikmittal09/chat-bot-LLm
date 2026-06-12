from tools.weather import get_weather
from tools.websearch import web_search

def run_get_weather(args):
    return get_weather(args["city"])

def run_web_search(args):
    return web_search(args["q"])

tool_map = {
    "get_weather": run_get_weather,
    "web_search":  run_web_search,
}