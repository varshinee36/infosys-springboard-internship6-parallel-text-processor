import os
import csv
import sqlite3
import matplotlib
matplotlib.use("Agg")  # non-interactive backend — safe for servers / multiprocessing
import matplotlib.pyplot as plt
 
from rule_engine import RULES
 
OUTPUT_DIR = "output"
 
 
def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
# ── CSV ───────────────────────────────────────────────────────────────────────
 
def save_csv(results: list, filename: str):
    """Save per-text rule match counts to CSV."""
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
 
    print(f"  [CSV] Saved → {path}  ({len(results)} rows)")
    return path
 
 
# ── SQLite ────────────────────────────────────────────────────────────────────
 
def save_to_db(results: list, table_name: str, db_path: str = None):
    """Save results to SQLite database."""
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
            tuple([row.get("_chunk_index", 0)] + [row.get(r, 0) for r in rule_names] + [total])
        )
 
    placeholders = ", ".join(["?"] * len(columns))
    cur.executemany(f"INSERT INTO {table_name} VALUES ({placeholders})", rows_to_insert)
    conn.commit()
    conn.close()
 
    print(f"  [DB]  Saved → {db_path}  table={table_name}  ({len(rows_to_insert)} rows)")
    return db_path
 
 
# ── Charts ────────────────────────────────────────────────────────────────────
 
def save_bar_chart(summary: dict, label: str, filename: str):
    """Bar chart: total matches per rule."""
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)
 
    total_per_rule = summary["total_per_rule"]
    rules = list(total_per_rule.keys())
    counts = [total_per_rule[r] for r in rules]
 
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(rules, counts, color="#2196F3", edgecolor="white", linewidth=0.8)
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_title(f"Total Rule Matches — {label}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Rule Category", fontsize=11)
    ax.set_ylabel("Total Keyword Matches", fontsize=11)
    ax.set_xticklabels(rules, rotation=25, ha="right", fontsize=9)
    ax.set_facecolor("#f9f9f9")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
 
    print(f"  [BAR] Saved → {path}")
    return path
 
 
def save_line_chart(summary: dict, label: str, filename: str):
    """Line chart: total matches per chunk (shows document flow / where keywords peak)."""
    ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, filename)
 
    per_chunk = summary["per_chunk_totals"]
    chunks = sorted(per_chunk.keys())
    values = [per_chunk[c] for c in chunks]
 
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(chunks, values, marker="o", color="#E91E63", linewidth=1.8,
            markersize=4, markerfacecolor="white", markeredgewidth=1.5)
    ax.fill_between(chunks, values, alpha=0.15, color="#E91E63")
    ax.set_title(f"Keyword Signal per Chunk — {label}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Chunk Index", fontsize=11)
    ax.set_ylabel("Total Keyword Matches", fontsize=11)
    ax.set_facecolor("#f9f9f9")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
 
    print(f"  [LINE] Saved → {path}")
    return path
 
 
# ── Terminal summary ──────────────────────────────────────────────────────────
 
def print_keyword_summary(summary: dict, label: str):
    """Print keyword summary and top 3 high-signal chunks to terminal."""
    print(f"\n{'='*55}")
    print(f"  KEYWORD SUMMARY — {label.upper()}")
    print(f"{'='*55}")
    for rule, count in summary["total_per_rule"].items():
        bar = "█" * min(count // 50, 30)
        print(f"  {rule:<22} {count:>6}  {bar}")
 
    print(f"\n  TOP 3 HIGH-SIGNAL CHUNKS:")
    per_chunk = summary["per_chunk_totals"]
    for rank, chunk_idx in enumerate(summary["top_chunks"], 1):
        print(f"    #{rank}  Chunk {chunk_idx:>4}  →  {per_chunk[chunk_idx]} matches")
    print(f"{'='*55}\n")