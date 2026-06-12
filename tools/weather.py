"""Get current weather for a city"""

def get_weather(city: str) -> str:
    """Fetch weather data using wttr.in API"""
    try:
        import requests
        response = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text}"
        return f"Unable to fetch weather for {city}"
    except Exception as e:
        return f"Weather error: {str(e)}"
