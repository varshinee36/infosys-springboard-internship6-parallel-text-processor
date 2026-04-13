import os
import json
import time
 
# ── Guard for multiprocessing on Windows ─────────────────────────────────────
if __name__ == "__main__":
 
    print("\n" + "=" * 60)
    print("  PARALLEL TEXT HANDLING PROCESSOR")
    print("  Disaster & Crisis Communication Monitor")
    print("=" * 60 + "\n")
 
    # ── 1. Preprocessing ──────────────────────────────────────────────────────
    from preprocessing import preprocess_tweets, preprocess_whatsapp
 
    print("[1/6] Preprocessing data…")
    tweet_texts = preprocess_tweets("data/tweets")
    whatsapp_texts, sender_counts = preprocess_whatsapp("data/whatsapp/Whatsapp_chat.csv")
 
    print(f"      Tweets loaded   : {len(tweet_texts):,}")
    print(f"      WA messages     : {len(whatsapp_texts):,}")
 
    # ── 2. NLP Benchmark (sequential vs parallel) ─────────────────────────────
    from processor import benchmark
 
    print("\n[2/6] NLP Benchmark — Tweets…")
    tweet_bench = benchmark(tweet_texts)
 
    print("\n[2/6] NLP Benchmark — WhatsApp…")
    wa_bench = benchmark(whatsapp_texts)
 
    # ── 3. Aggregate NLP insights ─────────────────────────────────────────────
    from aggregator import aggregate_results
 
    print("\n[3/6] Aggregating NLP insights…")
    tweet_insights = aggregate_results(tweet_bench["par_results"], label="Tweets")
    wa_insights    = aggregate_results(wa_bench["par_results"],    label="WhatsApp")
 
    tweet_insights["performance"] = {
        "sequential_time": tweet_bench["sequential_time"],
        "parallel_time":   tweet_bench["parallel_time"],
        "speedup":         tweet_bench["speedup"],
        "num_cores":       tweet_bench["num_cores"],
    }
    wa_insights["performance"] = {
        "sequential_time": wa_bench["sequential_time"],
        "parallel_time":   wa_bench["parallel_time"],
        "speedup":         wa_bench["speedup"],
        "num_cores":       wa_bench["num_cores"],
    }
    wa_insights["top_senders"] = dict(
        sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    )
 
    os.makedirs("data", exist_ok=True)
    with open("data/tweet_insights.json", "w") as f:
        json.dump(tweet_insights, f, indent=2)
    with open("data/whatsapp_insights.json", "w") as f:
        json.dump(wa_insights, f, indent=2)
    print("      JSON insights saved → data/tweet_insights.json")
    print("      JSON insights saved → data/whatsapp_insights.json")
 
    # ── 4. Rule Engine ────────────────────────────────────────────────────────
    from rule_engine import run_rule_engine_parallel, summarise_rule_results
 
    print("\n[4/6] Running Regex Rule Engine…")
 
    print("      → Tweets rule engine…")
    tweet_rule_results = run_rule_engine_parallel(tweet_texts)
    tweet_summary      = summarise_rule_results(tweet_rule_results)
 
    print("      → WhatsApp rule engine…")
    wa_rule_results = run_rule_engine_parallel(whatsapp_texts)
    wa_summary      = summarise_rule_results(wa_rule_results)
 
    # ── 5. Save outputs ───────────────────────────────────────────────────────
    from output_generator import (
        save_csv, save_to_db,
        save_bar_chart, save_line_chart,
        print_keyword_summary,
    )
 
    print("\n[5/6] Saving outputs…")
 
    # CSV
    save_csv(tweet_rule_results, "tweet_results.csv")
    save_csv(wa_rule_results,    "whatsapp_results.csv")
 
    # SQLite DB
    save_to_db(tweet_rule_results, table_name="tweets")
    save_to_db(wa_rule_results,    table_name="whatsapp")
 
    # Charts — Tweets
    save_bar_chart(tweet_summary,  label="Tweets",   filename="tweet_barchart.png")
    save_line_chart(tweet_summary, label="Tweets",   filename="tweet_linechart.png")
 
    # Charts — WhatsApp
    save_bar_chart(wa_summary,  label="WhatsApp", filename="whatsapp_barchart.png")
    save_line_chart(wa_summary, label="WhatsApp", filename="whatsapp_linechart.png")
 
    # ── 6. Terminal summary ───────────────────────────────────────────────────
    print("\n[6/6] Generating terminal summaries…")
    print_keyword_summary(tweet_summary, label="Tweets")
    print_keyword_summary(wa_summary,    label="WhatsApp")
 
    # ── Done ──────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  ALL OUTPUTS SAVED TO: output/")
    print("  ├── tweet_results.csv")
    print("  ├── whatsapp_results.csv")
    print("  ├── results.db  (tables: tweets, whatsapp)")
    print("  ├── tweet_barchart.png")
    print("  ├── tweet_linechart.png")
    print("  ├── whatsapp_barchart.png")
    print("  └── whatsapp_linechart.png")
    print("\n  RUN DASHBOARD:")
    print("  streamlit run dashboard.py")
    print("=" * 60 + "\n")