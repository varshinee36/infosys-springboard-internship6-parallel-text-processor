import sqlite3
from collections import Counter


CUSTOM_STOPWORDS = {
    'rt', 'de', 'en', 'la', 'el', 'les', 'le', 'et', 'du',
    'al', 'los', 'las', 'un', 'una', 'que', 'es', 'se', 'por',
    'con', 'para', 'via', 'amp', 'u', 'ur', 'r', 'im', 'dont',
    'please', 'near', 'stay', 'check', 'need', 'get', 'one',
    'like', 'go', 'know', 'said', 'say', 'also', 'still'
}


# ─────────────────────────────────────────────────────────────
# ✅ REAL-TIME AGGREGATOR (NEW)
# ─────────────────────────────────────────────────────────────
class RealTimeAggregator:
    def __init__(self):
        self.total_messages = 0
        self.master_counter = Counter()
        self.sentiments = []

    def update(self, processed_result: dict):
        """
        Update stats using ONE live processed message
        """
        self.total_messages += 1

        # keywords
        keywords = processed_result.get("keywords", [])
        self.master_counter.update(keywords)

        # sentiment
        self.sentiments.append(processed_result.get("sentiment", 0.0))

    def get_stats(self):
        """
        Return live stats for dashboard
        """
        avg_sentiment = (
            sum(self.sentiments) / len(self.sentiments)
            if self.sentiments else 0
        )

        top_keywords = [
            (w, c) for w, c in self.master_counter.most_common(10)
            if w not in CUSTOM_STOPWORDS
        ]

        return {
            "total_messages": self.total_messages,
            "avg_sentiment": round(avg_sentiment, 3),
            "top_keywords": dict(top_keywords)
        }


# ─────────────────────────────────────────────────────────────
# EXISTING BATCH AGGREGATION (UNCHANGED)
# ─────────────────────────────────────────────────────────────
def aggregate_results(results: list, label: str) -> dict:

    master_counter = Counter()
    all_sentiments = []

    for result in results:
        master_counter += result.get('freq', Counter())
        all_sentiments.append(result.get('sentiment', 0.0))

    avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.0

    top_keywords = [
        (w, c) for w, c in master_counter.most_common(30)
        if w not in CUSTOM_STOPWORDS
    ][:20]

    print(f"\n  [{label}] Results:")
    print(f"  Total processed:   {len(results)}")
    print(f"  Average sentiment: {avg_sentiment:.3f}")
    print(f"  Top 5 keywords:    {[w for w, c in top_keywords[:5]]}")

    return {
        'label':          label,
        'total':          len(results),
        'top_keywords':   dict(top_keywords),
        'avg_sentiment':  round(avg_sentiment, 3),
        'master_counter': master_counter,
    }


# ─────────────────────────────────────────────────────────────
# OPTIONAL SQLITE SAVE (UNCHANGED)
# ─────────────────────────────────────────────────────────────
def save_to_sqlite(label: str, results: list, db_path: str = "data/crisis_insights.db"):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crisis_texts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            text TEXT,
            sentiment REAL
        )
    """)

    for r in results:
        cursor.execute("""
            INSERT INTO crisis_texts (label, text, sentiment)
            VALUES (?, ?, ?)
        """, (
            label,
            str(r.get('text', '')),
            r.get('sentiment', 0.0)
        ))

    conn.commit()
    conn.close()