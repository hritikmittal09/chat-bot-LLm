
from File_Explore import file_options

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
                
            ]

