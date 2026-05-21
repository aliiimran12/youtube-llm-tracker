# LLM YouTube Tracker — Report

## What This Project Does

This project automatically monitors five YouTube channels focused on large language models (LLMs), fetches transcripts from their videos, and uses the Gemini AI API to generate structured summaries. The results are displayed on a public website that updates automatically every 6 hours.

## Live Site

https://aliiimran12.github.io/youtube-llm-tracker

## Channels Tracked

- Andrej Karpathy — Deep technical LLM education, neural network walkthroughs
- Lex Fridman — Long-form interviews with AI researchers and practitioners
- Yannic Kilcher — ML paper analyses and LLM research breakdowns
- Two Minute Papers — Concise summaries of AI research papers
- AI Explained — LLM news, benchmarks, and capability analysis

## How Data Is Collected

The `fetcher.py` script uses the YouTube Data API v3 to retrieve the 5 most recent videos from each channel. For each video, it fetches the auto-generated transcript using the `youtube-transcript-api` Python library.

## How Summaries Are Produced

Transcripts are sent to Google's Gemini API (`gemini-2.5-flash` model) via `summarizer.py`. Gemini returns a structured JSON object containing:
- **Topics** — key subjects covered in the video
- **Summary** — one sentence describing what the creator actually says
- **LLM Themes** — which LLM themes the video relates to (e.g. training, inference, agents)

## How the Table Stays Current

A GitHub Actions workflow (`.github/workflows/update.yml`) runs `main.py` every 6 hours automatically. When new videos are detected, it updates `data.json` and commits it back to the repository. GitHub Pages then serves the updated `index.html` which reads from `data.json`.

## How to Run Locally

1. Clone the repository
2. Create a `config.py` file with your API keys:
```python
import os
YT_APIKEY = "your_youtube_api_key"
GEMINI_APIKEY = "your_gemini_api_key"
```
3. Install dependencies: