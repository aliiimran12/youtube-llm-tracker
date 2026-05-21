from google import genai
import config
import time
import json

def summarize(video):
    client = genai.Client(api_key=config.GEMINI_APIKEY)
    
    if not video.get("transcript"):
        return {
            "topics": "No transcript available",
            "summary": "No transcript available",
            "llm_themes": "Unknown"
        }
    
    prompt = f"""You are analyzing a YouTube video about AI and large language models.

Title: {video['title']}
Channel: {video['channel']}
Transcript: {video['transcript']}

Return a JSON object with exactly these fields:
- topics: a short comma-separated list of topics covered
- summary: one sentence describing what the creator actually says
- llm_themes: which LLM themes this relates to (e.g. training, inference, agents, benchmarks)

Return only the JSON, nothing else."""

    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    time.sleep(15)
    
    try:
        text = response.text.strip().strip("```json").strip("```").strip()
        return json.loads(text)
    except:
        return {
            "topics": "Parse error",
            "summary": response.text[:200],
            "llm_themes": "Unknown"
        }