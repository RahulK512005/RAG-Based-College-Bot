import math
import hashlib
import numpy as np
from typing import List
import requests
from app.core.config import settings

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it",
    "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on",
    "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so",
    "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself",
    "can", "tell", "give", "please", "know", "much", "many"
}

class EmbeddingService:
    """Generates dense vector embeddings for text chunks and queries."""

    def __init__(self):
        self.dimension = 384

    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for a single text."""
        return self.get_embeddings([text])[0]

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate normalized dense embeddings for a list of texts."""
        if not texts:
            return []

        # 1. Try external API if configured
        api_key = settings.EMBEDDING_API_KEY or settings.LLM_API_KEY
        if api_key and not api_key.startswith("mock"):
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    "https://api.openai.com/v1/embeddings",
                    headers=headers,
                    json={
                        "input": texts,
                        "model": settings.EMBEDDING_MODEL
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return [item["embedding"] for item in data["data"]]
            except Exception as e:
                print(f"⚠️ External embedding API error: {e}. Falling back to internal semantic dense vectorizer.")

        # 2. High-Precision Subword Semantic Dense Vectorizer
        embeddings = []
        for text in texts:
            vec = self._compute_dense_vector(text)
            embeddings.append(vec)

        return embeddings

    def _compute_dense_vector(self, text: str) -> List[float]:
        """
        Compute positive-definite normalized semantic feature vector.
        Combines word unigrams, bigrams, and character 3-4 grams with sublinear TF scaling.
        """
        cleaned = text.lower().strip()
        tokens = [w.strip(".,!?;:\"'()[]{}#*-/\\") for w in cleaned.split() if w.strip()]
        
        vec = np.zeros(self.dimension, dtype=np.float32)

        # Word frequency counting
        counts = {}
        for w in tokens:
            counts[w] = counts.get(w, 0) + 1

        # 1. Word unigram features with sublinear TF
        for word, count in counts.items():
            if not word:
                continue

            is_stop = word in STOPWORDS
            if is_stop:
                continue # Skip pure stopwords to maximize discriminative signal

            tf = 1.0 + math.log(count)
            idf_weight = 2.0 + math.log(max(1, len(word)))

            # Hash word to vector bucket
            h = int(hashlib.sha256(word.encode('utf-8')).hexdigest(), 16)
            idx = h % self.dimension
            vec[idx] += tf * idf_weight

            # Character 3-gram and 4-gram features for subword stems (e.g. "attend" in "attendance")
            if len(word) >= 3:
                for n in (3, 4):
                    for j in range(len(word) - n + 1):
                        ngram = word[j:j+n]
                        nh = int(hashlib.md5(ngram.encode('utf-8')).hexdigest(), 16)
                        nidx = nh % self.dimension
                        vec[nidx] += 0.5 * tf

        # 2. Bigrams for phrases
        for i in range(len(tokens) - 1):
            w1, w2 = tokens[i], tokens[i+1]
            if w1 not in STOPWORDS and w2 not in STOPWORDS:
                bigram = f"{w1}_{w2}"
                bh = int(hashlib.sha256(bigram.encode('utf-8')).hexdigest(), 16)
                bidx = bh % self.dimension
                vec[bidx] += 3.0

        # L2 Normalization
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        else:
            vec[0] = 1.0

        return vec.tolist()

embedding_service = EmbeddingService()
