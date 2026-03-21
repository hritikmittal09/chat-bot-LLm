from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.getFileInfo import get_files_info, schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_make_dir, schema_write_file
from callFuction import call_function
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

prompt = input("Enter prompt: ")

tool_map = {
    "get_files_info": get_files_info,
}


config = types.GenerateContentConfig(
    system_instruction=(
        "You are a helpful coding agent.\n"
        "Use get_files_info to list files when needed.\n"
        "Use get_file_content to read file contents when the user asks to open/read a file.\n"
        "use run_python_file to run a specific python file when needed when user asks run .\n"
        "use make_dir to make a directory when needed\n" 
        "use write_file to write or overwrite the files if needed\n"
        "Always call the appropriate tool instead of guessing file content.\n"
    ),
    tools=[
        types.Tool(
            function_declarations=[
                schema_get_files_info,
                schema_get_file_content,  # ✅ fixed
                schema_run_python_file,
                schema_make_dir,
                schema_write_file
            ]
        )
    ],
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
       res = call_function(function_call,False)
       print(res)

else :
    print(response.text)
    



    