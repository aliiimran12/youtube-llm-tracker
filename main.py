import json
import config
from fetcher import get_recent_videos, get_transcript
from summarizer import summarize

def run():
    all_videos = []
    
    for channel_id, channel_name in config.CHANNELS:
        print(f"Fetching videos from {channel_name}...")
        videos = get_recent_videos(channel_id, channel_name)
        
        for video in videos:
            print(f"  Getting transcript for: {video['title']}")
            video["transcript"] = get_transcript(video["video_id"])
            
            print(f"  Summarizing...")
            summary = summarize(video)
            video["topics"] = summary["topics"]
            video["summary"] = summary["summary"]
            video["llm_themes"] = summary["llm_themes"]
            
            del video["transcript"]
            all_videos.append(video)
            
            with open("data.json", "w") as f:
                json.dump(all_videos, f, indent=2)
    
    print(f"\nDone! {len(all_videos)} videos saved to data.json")

if __name__ == "__main__":
    run()