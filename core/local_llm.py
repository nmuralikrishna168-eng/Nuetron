import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL


class LocalLLM:
    """Interface for local Ollama LLM queries."""

    @staticmethod
    def query(prompt: str, system_prompt: str = "") -> str:
        """Query the local Ollama model."""
        try:
            res = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                },
                timeout=60,
            )
            return res.json().get("response", "No response from model")
        except Exception as e:
            return f"Ollama connection error: {e}"

    @staticmethod
    def query_with_context(prompt: str, context: str, system_prompt: str = "") -> str:
        """Query Ollama with additional context."""
        full_prompt = f"Context:\n{context}\n\nQuestion:\n{prompt}"
        return LocalLLM.query(full_prompt, system_prompt)
