# from collections import Counter


# def aggregate_results(results, label):
#     master_freq = Counter()
#     all_sentiments = []

#     for result in results:
#         master_freq += result['word_freq']
#         all_sentiments.append(result['sentiment'])

#     top_keywords = [word for word, count in master_freq.most_common(20)]
#     overall_sentiment = sum(all_sentiments) / len(all_sentiments)
#     total_processed = len(results)

#     print(f"\n  [{label}] Top 5 keywords: {top_keywords[:5]}")
#     print(f"  [{label}] Overall sentiment: {overall_sentiment:.3f}")
#     print(f"  [{label}] Total processed: {total_processed}")

#     return {
#         'top_keywords': top_keywords,
#         'overall_sentiment': round(overall_sentiment, 3),
#         'total_processed': total_processed
#     }


# if __name__ == '__main__':
#     from processor import sequential_process

#     sample = [
#         "flood water rising quickly need help",
#         "earthquake buildings collapsed rescue needed",
#         "wildfire spreading fast please evacuate",
#         "people trapped need rescue boats urgent",
#         "sos family stuck flood area send help"
#     ]

#     results = sequential_process(sample)
#     insights = aggregate_results(results, label="TEST")
#     print("\n  Full insights dictionary:")
#     print(" ", insights)


# ------------------------------------------------------------------------------------------------------------------

# from collections import Counter


# CUSTOM_STOPWORDS = {
#     'rt', 'de', 'en', 'la', 'el', 'les', 'le', 'et', 'du',
#     'al', 'los', 'las', 'un', 'una', 'que', 'es', 'se', 'por',
#     'con', 'para', 'via', 'amp', 'u', 'ur', 'r', 'im', 'dont',
#     'please', 'near', 'stay', 'check', 'need', 'get', 'one',
#     'like', 'go', 'know', 'said', 'say', 'also', 'still'
# }

# def aggregate_results(results, label):
#     """
#     Merges all parallel worker results into one final insight.
#     Input:  results — list of dictionaries from process_single()
#             label   — "TWEETS" or "WHATSAPP"
#     Output: dictionary with top keywords, average sentiment, total count
#     """

    
#     master_counter = Counter()

    
#     all_sentiments = []

    
#     total = len(results)

    
#     for result in results:

       
#         master_counter += result['word_freq']

        
#         all_sentiments.append(result['sentiment'])

   
#     avg_sentiment = sum(all_sentiments) / len(all_sentiments)

   
#     top_keywords = master_counter.most_common(20)


    
#     top_keywords = [(w, c) for w, c in top_keywords 
#                     if w not in CUSTOM_STOPWORDS]
    
    
#     top_keywords = top_keywords[:20]


    

    
#     print(f"\n  [{label}] Results:")
#     print(f"  Total texts processed: {total}")
#     print(f"  Overall sentiment:     {avg_sentiment:.2f}")
#     print(f"  Top 5 keywords:        {[w for w, c in top_keywords[:5]]}")

    
#     return {
#         'label': label,
#         'total': total,
#         'top_keywords': top_keywords,
#         'avg_sentiment': avg_sentiment,
#         'master_counter': master_counter
#     }


# if __name__ == "__main__":
#     from preprocessing import preprocess_tweets, preprocess_whatsapp
#     from processor import parallel_process

#     print("=" * 45)
#     print("Testing aggregator.py")
#     print("=" * 45)

#     # Load and process tweets
#     print("\nLoading and processing tweets...")
#     tweets = preprocess_tweets("data/tweets")
#     tweet_results = parallel_process(tweets)
#     tweet_insights = aggregate_results(tweet_results, label="TWEETS")

#     # Load and process WhatsApp
#     print("\nLoading and processing WhatsApp...")
#     messages, senders = preprocess_whatsapp("data/whatsapp/Whatsapp_chat.csv")
#     whatsapp_results = parallel_process(messages)
#     whatsapp_insights = aggregate_results(whatsapp_results, label="WHATSAPP")

#     print("\n" + "=" * 45)
#     print("FINAL INSIGHTS")
#     print("=" * 45)
#     print(f"\nTweet sentiment:    {tweet_insights['avg_sentiment']:.2f}")
#     print(f"WhatsApp sentiment: {whatsapp_insights['avg_sentiment']:.2f}")

#     print(f"\nTop tweet keywords:")
#     for word, count in tweet_insights['top_keywords'][:10]:
#         print(f"  {word}: {count}")

#     print(f"\nTop WhatsApp keywords:")
#     for word, count in whatsapp_insights['top_keywords'][:10]:
#         print(f"  {word}: {count}")  


# ---------------------------------------------------------------------------------------------------------------------------

# import sqlite3
# from collections import Counter


# CUSTOM_STOPWORDS = {
#     'rt', 'de', 'en', 'la', 'el', 'les', 'le', 'et', 'du',
#     'al', 'los', 'las', 'un', 'una', 'que', 'es', 'se', 'por',
#     'con', 'para', 'via', 'amp', 'u', 'ur', 'r', 'im', 'dont',
#     'please', 'near', 'stay', 'check', 'need', 'get', 'one',
#     'like', 'go', 'know', 'said', 'say', 'also', 'still'
# }


# def save_to_sqlite(label: str, results: list, db_path: str = "data/crisis_insights.db"):
#     """
#     Saves per-text results to SQLite database.
#     Table: crisis_texts (label, text, sentiment, crisis_type, rule_scores...)
#     This matches the database-storage approach from the reference projects.
#     """
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Create table
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS crisis_texts (
#             id          INTEGER PRIMARY KEY AUTOINCREMENT,
#             label       TEXT,
#             text        TEXT,
#             sentiment   REAL,
#             crisis_type TEXT,
#             flood       INTEGER,
#             earthquake  INTEGER,
#             wildfire    INTEGER,
#             medical     INTEGER,
#             rescue      INTEGER,
#             shelter     INTEGER,
#             damage      INTEGER
#         )
#     """)

#     # Insert each result
#     for r in results:
#         rs = r.get('rule_scores', {})
#         cursor.execute("""
#             INSERT INTO crisis_texts
#             (label, text, sentiment, crisis_type, flood, earthquake, wildfire, medical, rescue, shelter, damage)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             label,
#             r.get('text', ''),
#             r.get('sentiment', 0.0),
#             r.get('crisis_type', 'general'),
#             rs.get('flood', 0),
#             rs.get('earthquake', 0),
#             rs.get('wildfire', 0),
#             rs.get('medical', 0),
#             rs.get('rescue', 0),
#             rs.get('shelter', 0),
#             rs.get('damage', 0),
#         ))

#     conn.commit()
#     conn.close()
#     print(f"  Saved {len(results)} records to SQLite → {db_path}")


# def aggregate_results(results: list, label: str) -> dict:
#     """
#     Merges all parallel worker results into final insights.
#     Now includes:
#     - Top keywords (cleaned)
#     - Average sentiment
#     - Crisis category distribution (rule engine output)
#     - SQLite save
#     """

#     master_counter = Counter()
#     all_sentiments = []
#     crisis_distribution = Counter()
#     rule_totals = Counter()

#     for result in results:
#         # Word frequency
#         master_counter += result['word_freq']

#         # Sentiment
#         all_sentiments.append(result['sentiment'])

#         # Crisis classification
#         crisis_distribution[result['crisis_type']] += 1

#         # Rule scores aggregation
#         for category, count in result['rule_scores'].items():
#             rule_totals[category] += count

#     avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.0

#     # Clean top keywords
#     top_keywords = [
#         (w, c) for w, c in master_counter.most_common(30)
#         if w not in CUSTOM_STOPWORDS
#     ][:20]

#     # Print summary
#     print(f"\n  [{label}] Results:")
#     print(f"  Total processed:      {len(results)}")
#     print(f"  Average sentiment:    {avg_sentiment:.3f}")
#     print(f"  Top 5 keywords:       {[w for w, c in top_keywords[:5]]}")
#     print(f"  Crisis distribution:  {dict(crisis_distribution.most_common())}")
#     print(f"  Rule totals:          {dict(rule_totals.most_common())}")

#     # Save to SQLite
#     save_to_sqlite(label, results)

#     return {
#         'label':               label,
#         'total':               len(results),
#         'top_keywords':        top_keywords,
#         'avg_sentiment':       round(avg_sentiment, 3),
#         'crisis_distribution': dict(crisis_distribution),
#         'rule_totals':         dict(rule_totals),
#         'master_counter':      master_counter,
#     }


# if __name__ == "__main__":
#     from preprocessing import preprocess_tweets, preprocess_whatsapp
#     from processor import parallel_process

#     print("=" * 50)
#     print("Testing upgraded aggregator.py")
#     print("=" * 50)

#     tweets = preprocess_tweets("data/tweets")
#     tweet_results, _ = parallel_process(tweets)
#     tweet_insights = aggregate_results(tweet_results, label="TWEETS")

#     messages, senders = preprocess_whatsapp("data/whatsapp/Whatsapp_chat.csv")
#     whatsapp_results, _ = parallel_process(messages)
#     whatsapp_insights = aggregate_results(whatsapp_results, label="WHATSAPP")

#     print("\nCrisis distribution — Tweets:")
#     for k, v in tweet_insights['crisis_distribution'].items():
#         print(f"  {k}: {v}")



# =======================================================================================================================

import sqlite3
from collections import Counter
 
 
CUSTOM_STOPWORDS = {
    'rt', 'de', 'en', 'la', 'el', 'les', 'le', 'et', 'du',
    'al', 'los', 'las', 'un', 'una', 'que', 'es', 'se', 'por',
    'con', 'para', 'via', 'amp', 'u', 'ur', 'r', 'im', 'dont',
    'please', 'near', 'stay', 'check', 'need', 'get', 'one',
    'like', 'go', 'know', 'said', 'say', 'also', 'still'
}
 
 
def save_to_sqlite(label: str, results: list, db_path: str = "data/crisis_insights.db"):
    """
    Saves per-text results to SQLite database.
    Table: crisis_texts (label, text, sentiment, crisis_type, rule_scores...)
    This matches the database-storage approach from the reference projects.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
 
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crisis_texts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            label       TEXT,
            text        TEXT,
            sentiment   REAL,
            crisis_type TEXT,
            flood       INTEGER,
            earthquake  INTEGER,
            wildfire    INTEGER,
            medical     INTEGER,
            rescue      INTEGER,
            shelter     INTEGER,
            damage      INTEGER
        )
    """)
 
    # Insert each result
    for r in results:
        rs = r.get('rule_scores', {})
        cursor.execute("""
            INSERT INTO crisis_texts
            (label, text, sentiment, crisis_type, flood, earthquake, wildfire, medical, rescue, shelter, damage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            label,
            r.get('text', ''),
            r.get('sentiment', 0.0),
            r.get('crisis_type', 'general'),
            rs.get('flood', 0),
            rs.get('earthquake', 0),
            rs.get('wildfire', 0),
            rs.get('medical', 0),
            rs.get('rescue', 0),
            rs.get('shelter', 0),
            rs.get('damage', 0),
        ))
 
    conn.commit()
    conn.close()
    print(f"  Saved {len(results)} records to SQLite → {db_path}")
 
 
def aggregate_results(results: list, label: str) -> dict:
    """
    Merges all parallel worker results into final insights.
    Processor returns: {'freq': Counter, 'sentiment': float, 'token_count': int}
    """
 
    master_counter = Counter()
    all_sentiments = []
 
    for result in results:
        # processor.py uses 'freq' as the key (Counter of word frequencies)
        master_counter += result.get('freq', Counter())
 
        # sentiment is a float from TextBlob
        all_sentiments.append(result.get('sentiment', 0.0))
 
    avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.0
 
    # Clean top keywords — remove custom stopwords
    top_keywords = [
        (w, c) for w, c in master_counter.most_common(30)
        if w not in CUSTOM_STOPWORDS
    ][:20]
 
    # Print summary
    print(f"\n  [{label}] Results:")
    print(f"  Total processed:   {len(results)}")
    print(f"  Average sentiment: {avg_sentiment:.3f}")
    print(f"  Top 5 keywords:    {[w for w, c in top_keywords[:5]]}")
 
    return {
        'label':          label,
        'total':          len(results),
        'top_keywords':   dict(top_keywords),   # dict for JSON serialisation
        'avg_sentiment':  round(avg_sentiment, 3),
        'master_counter': master_counter,
    }
 
 
if __name__ == "__main__":
    from preprocessing import preprocess_tweets, preprocess_whatsapp
    from processor import parallel_process
 
    print("=" * 50)
    print("Testing upgraded aggregator.py")
    print("=" * 50)
 
    tweets = preprocess_tweets("data/tweets")
    tweet_results, _ = parallel_process(tweets)
    tweet_insights = aggregate_results(tweet_results, label="TWEETS")
 
    messages, senders = preprocess_whatsapp("data/whatsapp/Whatsapp_chat.csv")
    whatsapp_results, _ = parallel_process(messages)
    whatsapp_insights = aggregate_results(whatsapp_results, label="WHATSAPP")
 
    print("\nCrisis distribution — Tweets:")
    for k, v in tweet_insights['crisis_distribution'].items():
        print(f"  {k}: {v}")
