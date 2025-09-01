# agents/rag_agent.py

import os
import faiss
import numpy as np
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from core.event_bus import EventBus


class RAGAgent:
    def __init__(self, bus: EventBus):
        self.bus = bus
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Initialize ChromaDB client
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("songs")

        # FAISS index setup (embedding size = 384 for MiniLM)
        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)

        # OpenAI client
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Subscribe to events
        self.bus.subscribe("user_query", self.handle_query)

    def embed(self, text: str) -> np.ndarray:
        return self.model.encode([text])[0]

    def add_song(self, song_id: str, title: str, metadata: dict):
        """Add song embeddings to both FAISS and Chroma."""
        embedding = self.embed(title).astype("float32")
        self.index.add(np.array([embedding]))
        self.collection.add(documents=[title], ids=[song_id], metadatas=[metadata])

    def search(self, query: str, top_k: int = 3):
        """Search FAISS + Chroma for song candidates."""
        q_emb = self.embed(query).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.collection.get()["ids"]):
                data = self.collection.get()["metadatas"][idx]
                results.append(data)
        return results

    def handle_query(self, query: str):
        """Handle user voice query, run retrieval, and publish results."""
        results = self.search(query)
        if results:
            print("RAGAgent retrieved:", results)
            self.bus.publish("rag_results", results)
        else:
            print("No results found.")
            self.bus.publish("rag_results", [])
