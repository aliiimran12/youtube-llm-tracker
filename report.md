# LLM YouTube Tracker — Report

## Live Site
https://aliiimran12.github.io/youtube-llm-tracker

## GitHub Repository
https://github.com/aliiimran12/youtube-llm-tracker

## What This Project Does

This project automatically monitors five YouTube channels focused on large language models (LLMs), fetches transcripts from their videos, and uses the Google Gemini AI API to generate structured summaries. The results are displayed on a live public website that updates automatically every 6 hours via GitHub Actions.

## Channels Tracked

- **Andrej Karpathy** — Deep technical LLM education, neural network walkthroughs from a former OpenAI and Tesla AI lead
- **Lex Fridman** — Long-form interviews with leading AI researchers and practitioners
- **Yannic Kilcher** — ML paper analyses and LLM research breakdowns
- **Two Minute Papers** — Concise summaries of the latest AI research papers
- **AI Explained** — LLM news, benchmarks, and capability analysis

## How Data Is Collected

`fetcher.py` uses the YouTube Data API v3 to retrieve the 3 most recent videos from each channel. For each video, it fetches the auto-generated transcript using the `youtube-transcript-api` Python library. A 3-second delay is added between transcript requests to reduce the chance of IP-based rate limiting by YouTube.

## How Summaries Are Produced

Transcripts are sent to Google's Gemini API (`gemini-2.5-flash` model) via `summarizer.py`. A carefully structured prompt asks Gemini to return a JSON object containing:
- **Topics** — key subjects covered in the video
- **Summary** — one sentence describing what the creator actually says based on the transcript, not just the title
- **LLM Themes** — which LLM themes the video relates to (e.g. training, inference, agents, benchmarks)

A 15-second delay is added between Gemini requests to stay within the free tier rate limit of 5 requests per minute.

## How the Table Stays Current

A GitHub Actions workflow (`.github/workflows/update.yml`) runs `main.py` every 6 hours automatically on a cron schedule (`0 */6 * * *`). When new videos are detected, `data.json` is updated and committed back to the repository. GitHub Pages serves `index.html` which reads from `data.json` on every page load, so the site always reflects the latest data.

## Known Limitations & How They Were Handled

**YouTube transcript IP blocking:** YouTube aggressively rate-limits transcript requests from IPs that make too many requests in a short period. This affected both local development and GitHub Actions runs. The system handles this gracefully — videos where transcripts are unavailable are still listed in the table with a "No transcript available" note, rather than crashing. The next scheduled run will attempt those videos again.

**Gemini free tier quota:** The free tier allows 20 requests per day. With 15 videos tracked and a 15-second delay between requests, a full run uses exactly 15 requests, staying safely within quota. Earlier in development, running the script multiple times during testing exhausted the daily quota, which has since been addressed by reducing `MAX_VIDS_PERCHANNEL` from 5 to 3.

**API key security:** During early development, API keys were accidentally committed to the public GitHub repository before `.gitignore` was configured correctly. The exposed keys were immediately revoked and replaced, git history was purged using `git filter-branch`, and all keys are now stored exclusively as GitHub Actions secrets and local environment variables — never in the codebase.

## Why OpenClaw Was Not Used

The original brief suggested OpenClaw as the automated watcher. During setup on Windows, OpenClaw encountered a critical error where the managed Codex app-server binary (`@openai/codex`) was not found, preventing the agent from running despite the gateway starting successfully. After attempting multiple fixes including reinstalling dependencies and adjusting execution policies, the decision was made to build an equivalent Python-based watcher instead — as explicitly permitted by the brief ("or an equivalent automated watcher you choose"). The resulting Python pipeline covers all the same functionality: channel monitoring, transcript fetching, AI summarization, and scheduled automation.

## How to Run Locally

1. Clone the repository
2. Create a `config.py` file with your API keys:
```python
import os
YT_APIKEY = os.environ.get("YT_APIKEY", "your_youtube_api_key")
GEMINI_APIKEY = os.environ.get("GEMINI_APIKEY", "your_gemini_api_key")
CHANNELS = [
    ("UCXUPKJO5MZQN11PqgIvyuvQ", "Andrej Karpathy"),
    ("UCSHZKyawb77ixDdsGog4iWA", "Lex Fridman"),
    ("UCZHmQk67mSJgfCCTn7xBfew", "Yannic Kilcher"),
    ("UCbfYPyITQ-7l4upoX8nvctg", "Two Minute Papers"),
    ("UCNJ1Ymd5yFuUPtn21xtRbbw", "AI Explained"),
]
MAX_VIDS_PERCHANNEL = 3
```
3. Install dependencies:
pip install google-api-python-client youtube-transcript-api google-genai
4. Run the tracker:
python main.py

## Tech Stack

- Python 3.11
- YouTube Data API v3
- youtube-transcript-api
- Google Gemini API (gemini-2.5-flash)
- GitHub Actions (automated scheduling)
- GitHub Pages (public hosting)