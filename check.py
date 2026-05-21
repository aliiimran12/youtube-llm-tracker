from google import genai
import config

client = genai.Client(api_key=config.GEMINI_APIKEY)
for model in client.models.list():
    print(model.name)