


tools_schemas = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get weather of a city",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string"}
                            },
                            "required": ["city"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "web_search",
                        "description": "Search the internet ONLY for current or real-time information that cannot be answered from the model's knowledge. Do not use for greetings, coding help, math, or general conversation.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "q": {"type": "string", "description": "Search query to find information on the web"}
                            },
                            "required": ["q"]
                        }
                    }
                }
            ]