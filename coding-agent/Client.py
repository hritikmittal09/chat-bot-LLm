from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.getFileInfo import get_files_info, schema_get_files_info

import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

prompt = input("Enter prompt: ")

tool_map = {
    "get_files_info": get_files_info,
}


config = types.GenerateContentConfig(
    system_instruction="You are a helpful coding agent. Use the get_files_info tool to list files when asked.",
    tools=[types.Tool(function_declarations=[schema_get_files_info])],  # ✅ wrap it
)

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)]),
]

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=messages,
        config=config,
    )

if response.function_calls:
    for function_call in response.function_calls:
       print( f"calling function- {function_call.name} {function_call.args}")
else :
    print(response.text)
    



    