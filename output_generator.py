import os
import csv
import sqlite3
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from datetime import datetime
from rule_engine import RULES

OUTPUT_DIR = "output"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# ✅ REAL-TIME LOGGING (NEW)
# ─────────────────────────────────────────────────────────────
def log_realtime_message(text: str, alert: str, filename="realtime_log.csv"):
    """
    Append live messages to CSV (for real-time tracking)
    """
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)

    file_exists = os.path.isfile(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "message", "alert_level"])

        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), text, alert])

    return path


# ─────────────────────────────────────────────────────────────
# EXISTING CSV
# ─────────────────────────────────────────────────────────────
def save_csv(results: list, filename: str):
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)

    rule_names = list(RULES.keys())
    fieldnames = ["chunk_index"] + rule_names + ["total_matches"]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in results:
            total = sum(row.get(r, 0) for r in rule_names)
            writer.writerow({
                "chunk_index": row.get("_chunk_index", 0),
                **{r: row.get(r, 0) for r in rule_names},
                "total_matches": total,
            })

    print(f"  [CSV] Saved → {path}")
    return path


# ─────────────────────────────────────────────────────────────
# SQLITE
# ─────────────────────────────────────────────────────────────
def save_to_db(results: list, table_name: str, db_path: str = None):

    ensure_output_dir()
    if db_path is None:
        db_path = os.path.join(OUTPUT_DIR, "results.db")

    rule_names = list(RULES.keys())
    columns = ["chunk_index"] + rule_names + ["total_matches"]
    col_defs = ", ".join(f"{c} INTEGER" for c in columns)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"CREATE TABLE {table_name} ({col_defs})")

    rows_to_insert = []
    for row in results:
        total = sum(row.get(r, 0) for r in rule_names)
        rows_to_insert.append(
            tuple([row.get("_chunk_index", 0)] +
                  [row.get(r, 0) for r in rule_names] +
                  [total])
        )

    placeholders = ", ".join(["?"] * len(columns))
    cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows_to_insert)

    conn.commit()
    conn.close()

    print(f"  [DB] Saved → {db_path}")
    return db_path


# ─────────────────────────────────────────────────────────────
# REAL-TIME STATS (NEW)
# ─────────────────────────────────────────────────────────────
def get_realtime_stats(filename="realtime_log.csv"):
    """
    Load live messages and return stats
    """
    path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(path):
        return {}

    import pandas as pd
    df = pd.read_csv(path)

    return {
        "total_messages": len(df),
        "high_alerts": len(df[df["alert_level"].str.contains("HIGH", na=False)]),
        "medium_alerts": len(df[df["alert_level"].str.contains("MEDIUM", na=False)]),
    }


# ─────────────────────────────────────────────────────────────
# CHARTS (UNCHANGED)
# ─────────────────────────────────────────────────────────────
def save_bar_chart(summary: dict, label: str, filename: str):
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)

    total_per_rule = summary["total_per_rule"]
    rules = list(total_per_rule.keys())
    counts = [total_per_rule[r] for r in rules]

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(rules, counts)

    ax.set_title(f"Total Rule Matches — {label}")
    ax.set_xticklabels(rules, rotation=25)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

    return path


def save_line_chart(summary: dict, label: str, filename: str):
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)

    per_chunk = summary["per_chunk_totals"]
    chunks = sorted(per_chunk.keys())
    values = [per_chunk[c] for c in chunks]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(chunks, values)

    ax.set_title(f"Keyword Signal per Chunk — {label}")

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

    return path


# ─────────────────────────────────────────────────────────────
# TERMINAL SUMMARY
# ─────────────────────────────────────────────────────────────
def print_keyword_summary(summary: dict, label: str):

    print(f"\n{'='*50}")
    print(f"KEYWORD SUMMARY — {label}")
    print(f"{'='*50}")

    for rule, count in summary["total_per_rule"].items():
        print(f"{rule:<20} : {count}")

    print("\nTop chunks:")
    for chunk in summary["top_chunks"]:
        print(f"  Chunk {chunk}")