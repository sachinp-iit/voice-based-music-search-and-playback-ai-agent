# agents/youtube_agent.py

import yt_dlp
import os
import tempfile
import vlc
from core.event_bus import EventBus


class YouTubeAgent:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.player = None

        # Subscribe to RAG results
        self.bus.subscribe("rag_results", self.handle_rag_results)

    def search_and_play(self, query: str):
        """Search YouTube and play the first matching result."""
        print(f"YouTubeAgent: Searching for {query}")

        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "quiet": True,
            "default_search": "ytsearch1",  # search and return 1 result
            "outtmpl": os.path.join(tempfile.gettempdir(), "%(title)s.%(ext)s"),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if "entries" in info:
                info = info["entries"][0]

            file_path = ydl.prepare_filename(info)

        print(f"Playing {info['title']} from YouTube...")

        # Play with VLC
        self.player = vlc.MediaPlayer(file_path)
        self.player.play()

    def stop(self):
        """Stop playback if running."""
        if self.player:
            self.player.stop()

    def handle_rag_results(self, results):
        """Handle RAG search results, take top result, and play via YouTube."""
        if not results:
            print("YouTubeAgent: No RAG results to play.")
            return

        top_result = results[0]
        query = top_result.get("title") or top_result.get("name", "")
        if query:
            self.search_and_play(query)
