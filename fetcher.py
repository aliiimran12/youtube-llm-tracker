from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import config

youtube = build("youtube", "v3", developerKey=config.YT_APIKEY)

def get_recent_videos(channel_id, channel_name):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=config.MAX_VIDS_PERCHANNEL,
        order="date",
        type="video"
    )
    response = request.execute()
    
    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        published = item["snippet"]["publishedAt"][:10]
        videos.append({
            "video_id": video_id,
            "title": title,
            "published": published,
            "channel": channel_name,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        })
    return videos

def get_transcript(video_id):
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)
        text = " ".join([entry.text for entry in transcript])
        return text[:10000]
    except Exception as e:
        print(f"    Transcript error: {e}")
        return None