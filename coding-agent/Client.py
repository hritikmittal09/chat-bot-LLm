from google import genai
from dotenv import load_dotenv
from google.genai import types
from functions.getFileInfo import get_files_info
import os

load_dotenv()

GAMINI_API_KEY = os.getenv("GAMNI_API-KEY")

print(get_files_info("Calculartor/pkg"))
prompt = input("enter prompt")
messages =[
     types.Content(role="user", parts=[types.Part(text=prompt)])
]

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GAMINI_API_KEY)

response = client.models.generate_content(
model="gemini-2.5-flash-lite",
 contents= messages
)
print(response.text)