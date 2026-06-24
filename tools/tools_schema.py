
from File_Explore import file_options
from tools.Memory.create_memory import memory_keys

open_file_schema = {
    "type": "function",
    "function": {
        "name": "open_file",
        "description": "Open a local file, folder, or website from predefined shortcuts.",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": f"Shortcut name of the file, folder, or website to open  you can open {file_options()} with this tools"
                }
            },
            "required": ["fileName"]
        }
    }
}


get_memery =  {
        "type": "function",
        "function": {
            "name": "memory",
            "description": (
                "Retrieve stored memory information from Memory.json "
                f"using a specific key. you have {memory_keys()} to chose from "
                "Use this tool whenever the user asks about saved preferences, "
                "past conversations, personal details, or previously stored data. "
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": (
                            "The memory key to search for inside Memory.json. "
                            "Example: 'name', 'skills', 'project', 'favorite_language'"
                        )
                    }
                },
                "required": ["key"]
            }
        }
    }



web_search_schema = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the internet ONLY for current or real-time information that cannot be answered from the model's knowledge. Do not use for greetings, coding help, math, or general conversation.",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Search query to find information on the web"
                }
            },
            "required": ["q"]
        }
    }
}
get_eeather_sechma = {
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
                }






tools_schemas = [
                open_file_schema,
                get_eeather_sechma,
                web_search_schema,
                #get_memery
                
            ]

