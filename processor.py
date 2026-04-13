import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed

import nltk
from textblob import TextBlob

# ── Ensure NLTK data ─────────────────────────────────────────────────────────
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

ENGLISH_STOPWORDS = set(stopwords.words("english"))
EXTRA_STOPWORDS = {
    "rt", "de", "en", "la", "el", "que", "es", "un", "una", "le", "les",
    "http", "https", "amp", "via", "co", "t", "s", "u", "r", "like", "just",
    "get", "got", "know", "go", "one", "would", "also", "us", "im", "dont",
    "cant", "wont", "ive", "its", "thats", "via", "im",
}
ALL_STOPWORDS = ENGLISH_STOPWORDS | EXTRA_STOPWORDS

N_WORKERS = 4


# ─────────────────────────────────────────────────────────────
# ✅ REAL-TIME SINGLE TEXT PROCESSING (NEW)
# ─────────────────────────────────────────────────────────────
def process_single_realtime(text: str) -> dict:
    """
    Fast processing for live dashboard input.
    """
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in ALL_STOPWORDS and len(t) > 2]

    freq = Counter(tokens)
    sentiment = TextBlob(text).sentiment.polarity

    return {
        "keywords": list(freq.keys())[:5],
        "sentiment": sentiment,
        "token_count": len(tokens)
    }


# ─────────────────────────────────────────────────────────────
# EXISTING (UNCHANGED CORE)
# ─────────────────────────────────────────────────────────────
def process_single(text: str) -> dict:
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in ALL_STOPWORDS and len(t) > 2]
    freq = Counter(tokens)
    sentiment = TextBlob(text).sentiment.polarity
    return {"freq": freq, "sentiment": sentiment, "token_count": len(tokens)}


def process_chunk(chunk: list) -> list:
    return [process_single(text) for text in chunk]


def _worker(args):
    chunk_idx, chunk = args
    return chunk_idx, process_chunk(chunk)


# ─────────────────────────────────────────────────────────────
# PARALLEL PROCESSING
# ─────────────────────────────────────────────────────────────
def parallel_process(data: list) -> list:

    chunk_size = max(1, len(data) // N_WORKERS)
    chunks = [(i, data[i * chunk_size:(i + 1) * chunk_size]) for i in range(N_WORKERS)]

    remainder = data[N_WORKERS * chunk_size:]
    if remainder:
        chunks.append((N_WORKERS, remainder))

    ordered = {}
    with ProcessPoolExecutor(max_workers=N_WORKERS) as executor:
        futures = {executor.submit(_worker, c): c[0] for c in chunks}
        for future in as_completed(futures):
            idx, result = future.result()
            ordered[idx] = result

    flat = []
    for key in sorted(ordered.keys()):
        flat.extend(ordered[key])
    return flat


# ─────────────────────────────────────────────────────────────
# SEQUENTIAL (FOR BENCHMARK)
# ─────────────────────────────────────────────────────────────
def sequential_process(data: list) -> list:
    return [process_single(text) for text in data]


# ─────────────────────────────────────────────────────────────
# BENCHMARK
# ─────────────────────────────────────────────────────────────
def benchmark(data: list) -> dict:

    print(f"  Running sequential on {len(data)} texts…")
    t0 = time.time()
    seq_results = sequential_process(data)
    seq_time = round(time.time() - t0, 2)

    print(f"  Running parallel ({N_WORKERS} workers) on {len(data)} texts…")
    t0 = time.time()
    par_results = parallel_process(data)
    par_time = round(time.time() - t0, 2)

    speedup = round(seq_time / par_time, 2) if par_time > 0 else 1.0

    print(f"  Sequential: {seq_time}s  |  Parallel: {par_time}s  |  Speedup: {speedup}x")

    return {
        "seq_results": seq_results,
        "par_results": par_results,
        "sequential_time": seq_time,
        "parallel_time": par_time,
        "speedup": speedup,
        "num_cores": N_WORKERS,
    }