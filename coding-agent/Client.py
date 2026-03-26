from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.getFileInfo import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_make_dir, schema_write_file
from callFuction import call_function
import os

load_dotenv()

def coding_agent_client(Input_propmt = None):
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL = os.getenv("MODEL")

    if Input_propmt !=None :
        prompt = Input_propmt
    else :    

        prompt = input("Enter prompt: ")

    config = types.GenerateContentConfig(
        system_instruction=(
            "You are a helpful coding agent.\n"
            "Use get_files_info to list files when needed.\n"
            "Use get_file_content to read file contents when the user asks to open/read a file.\n"
            "use run_python_file to run a specific python file when needed when user asks run.\n"
            "use make_dir to make a directory when needed\n"
            "use write_file to write or overwrite the files if needed\n"
            "Always call the appropriate tool instead of guessing file content.\n"
        ),
        tools=[
            types.Tool(
                function_declarations=[
                    schema_get_files_info,
                    schema_get_file_content,
                    schema_run_python_file,
                    schema_make_dir,
                    schema_write_file,
                ]
            )
        ],
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    client = genai.Client(api_key=GEMINI_API_KEY)

    # ✅ agent loop — max 20 iterations for safety
    for i in range(10):
        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=config,
        )

        # ✅ safety check
        candidate = response.candidates[0]
        if candidate.content is None or candidate.content.parts is None:
            print("No response, reason:", candidate.finish_reason)
            break

        # no tool calls = final answer
        if not response.function_calls:
            print(response.text)
            break

        # append model response to history
        messages.append(candidate.content)

        # run tools and collect results
        tool_results = []
        for function_call in response.function_calls:
            print(f"🔧 calling: {function_call.name}({function_call.args})")
            result = call_function(function_call, verbose=False)
            print(f"   → {result}")
            tool_results.append(
        types.Part(
            function_response=types.FunctionResponse(
                name=function_call.name,
                response={"result": str(result)},  # ← force string
            )
        )
    )

        # send results back
        messages.append(
            types.Content(role="user", parts=tool_results)
        )
if __name__ == "__main__":
    coding_agent_client()        
