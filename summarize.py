# summarize.py

import re
from collections import Counter

def summarize_text(text, max_sentences=6):
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Ignore common filler words
    ignore = set(["the", "and", "a", "to", "of", "in", "is", "it", "on", "for", "as", "was", "with", "that"])

    # Word frequency scoring
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(w for w in words if w not in ignore)

    scored = []
    for sentence in sentences:
        score = sum(word_freq.get(w.lower(), 0) for w in sentence.split())
        scored.append((score, sentence))

    # Pick best sentences
    best_sentences = [s for score, s in sorted(scored, reverse=True)[:max_sentences]]

    # Sort sentences back to original reading order
    best_sentences = sorted(best_sentences, key=lambda s: sentences.index(s))

    # Join as **natural paragraph (like LangSearch)**
    summary = " ".join(best_sentences).strip()

    # Cleanup formatting
    summary = re.sub(r'\s+', ' ', summary)

    return summary
