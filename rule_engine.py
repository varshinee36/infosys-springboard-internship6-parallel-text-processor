import re
from concurrent.futures import ProcessPoolExecutor, as_completed

# ── Disaster keyword rules ────────────────────────────────────────────────────
RULES = {
    "distress_signals":  r"\b(help|trapped|rescue|sos|urgent|missing|survivor|stranded|emergency|mayday)\b",
    "disaster_types":    r"\b(flood|earthquake|fire|cyclone|tsunami|hurricane|tornado|landslide|wildfire|drought)\b",
    "locations":         r"\b(road|river|village|colony|district|bridge|building|hospital|school|shelter)\b",
    "resources":         r"\b(food|water|boat|ambulance|shelter|medicine|clothes|blanket|supply|aid)\b",
    "sentiment_words":   r"\b(danger|dangerous|safe|safety|critical|improving|severe|deadly|devastating|hopeful)\b",
    "action_keywords":   r"\b(evacuate|evacuated|deployed|rescue|relief|respond|alert|warn|coordinate)\b",
    "infrastructure":    r"\b(power|electricity|network|communication|highway|airport|port|dam|pipeline|grid)\b",
}


# ── SINGLE TEXT RULE APPLICATION (NEW - for real-time) ────────────────────────
def apply_rules_single(text: str) -> dict:
    """
    Apply rules to a single message (used for real-time input).
    Returns {rule_name: count}
    """
    text_lower = text.lower()
    return {rule: len(re.findall(pattern, text_lower)) for rule, pattern in RULES.items()}


# ── ALERT DETECTION (NEW) ─────────────────────────────────────────────────────
def detect_alert_level(rule_counts: dict) -> str:
    """
    Determine alert level based on rule matches.
    """
    if rule_counts.get("distress_signals", 0) > 0:
        return "HIGH 🚨"
    elif rule_counts.get("disaster_types", 0) > 0:
        return "MEDIUM ⚠️"
    else:
        return "LOW ✅"


# ── EXISTING FUNCTIONS (UNCHANGED) ────────────────────────────────────────────
def apply_rules(text: str) -> dict:
    """Apply all rules to a single text string. Returns {rule_name: count}."""
    text_lower = text.lower()
    return {rule: len(re.findall(pattern, text_lower)) for rule, pattern in RULES.items()}


def apply_rules_to_chunk(args):
    """
    Worker function: apply rules to a list of texts (one chunk).
    Returns list of dicts — one per text.
    """
    chunk_index, texts = args
    results = []
    for text in texts:
        counts = apply_rules(text)
        counts["_chunk_index"] = chunk_index
        results.append(counts)
    return chunk_index, results


def run_rule_engine_parallel(data: list, n_workers: int = 4) -> list:
    """
    Split data into chunks and apply rules in parallel using ProcessPoolExecutor.
    Returns list of per-text rule count dicts, in original order.
    """
    chunk_size = max(1, len(data) // n_workers)
    chunks = [
        (i, data[i * chunk_size: (i + 1) * chunk_size])
        for i in range(n_workers)
    ]

    # Handle remainder
    remainder = data[n_workers * chunk_size:]
    if remainder:
        chunks.append((n_workers, remainder))

    ordered_results = {}
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(apply_rules_to_chunk, chunk): chunk[0] for chunk in chunks}
        for future in as_completed(futures):
            chunk_index, chunk_results = future.result()
            ordered_results[chunk_index] = chunk_results

    # Flatten in order
    flat = []
    for key in sorted(ordered_results.keys()):
        flat.extend(ordered_results[key])
    return flat


def summarise_rule_results(results: list) -> dict:
    """
    Aggregate per-text results into:
      - total_per_rule: {rule: total_count}
      - per_chunk_totals: {chunk_index: total_matches}
      - top_chunks: top 3 chunk indices by total matches
    """
    total_per_rule = {rule: 0 for rule in RULES}
    per_chunk_totals = {}

    for row in results:
        chunk_idx = row.get("_chunk_index", 0)
        chunk_sum = 0
        for rule in RULES:
            count = row.get(rule, 0)
            total_per_rule[rule] += count
            chunk_sum += count
        per_chunk_totals[chunk_idx] = per_chunk_totals.get(chunk_idx, 0) + chunk_sum

    top_chunks = sorted(per_chunk_totals, key=per_chunk_totals.get, reverse=True)[:3]

    return {
        "total_per_rule": total_per_rule,
        "per_chunk_totals": per_chunk_totals,
        "top_chunks": top_chunks,
    }