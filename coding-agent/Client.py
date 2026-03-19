from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GAMINI_API_KEY = os.getenv("GAMNI_API-KEY")
prompt = input("enter prompt")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key=GAMINI_API_KEY)

response = client.models.generate_content(
model="gemini-2.5-flash-lite", contents= f"{prompt}7"
)
print(response.text)