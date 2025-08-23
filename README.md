# Voice Based Bollywood Song Search & Playback AI Agent

This repository contains an AI Agent system that allows users to **search and play Bollywood songs via voice commands** using GPT-4o-mini, FAISS/Chroma for retrieval, and event-based agent communication (Google-style Agent-to-Agent protocol).

## Features
- **Voice Input**: Users request songs using speech (STT).  
- **Song Retrieval**: Finds Bollywood songs via APIs or vector DB (FAISS + Chroma).  
- **Agent Collaboration**: Agents communicate using Google Agent-to-Agent protocol (event/message passing).  
- **Playback**: Streams Bollywood songs with user consent.  
- **Memory**: Maintains user song history for personalized recommendations.  

## Agent Architecture
1. **Voice Agent** → Converts voice to text.  
2. **Retrieval Agent** → Searches songs.  
3. **Suggestion Agent** → Suggests based on history.  
4. **Playback Agent** → Plays the selected song.  

## Flow Example
1. User says: *"Play Kal Ho Na Ho"*.  
2. System retrieves and plays the song.  
3. Next time, user says: *"Play something similar"*.  
4. Suggestion Agent recommends related songs.  

## Repository Name Suggestions
- `rag-music-agent`
- `voice2song`
- `song-rag-ai`
- `melody-agent`

## Setup
```bash
# Clone repository
git clone https://github.com/your-username/rag-music-agent.git
cd rag-music-agent

# Install dependencies
pip install -r requirements.txt
```

## Run
```bash
python main.py
```
