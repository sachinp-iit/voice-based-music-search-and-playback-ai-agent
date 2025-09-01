# agents/playback_agent.py

import vlc
import yt_dlp
from core.event_bus import EventBus

class PlaybackAgent:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.bus.subscribe("youtube_result", self.handle_youtube_result)
        self.player = None

    def handle_youtube_result(self, video_url: str):
        """Handles YouTube video URL and plays it with user consent."""
        print(f"Song found: {video_url}")
        consent = input("Do you want to play this song? (y/n): ").strip().lower()

        if consent == "y":
            self.play_song(video_url)
        else:
            print("Playback skipped by user.")

    def play_song(self, video_url: str):
        """Stream audio from YouTube using yt_dlp + VLC."""
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "no_warnings": True,
            "default_search": "ytsearch",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info["url"]

        print("Playing song...")
        self.player = vlc.MediaPlayer(audio_url)
        self.player.play()

    def stop(self):
        """Stop playback if running."""
        if self.player:
            self.player.stop()
            print("Playback stopped.")
