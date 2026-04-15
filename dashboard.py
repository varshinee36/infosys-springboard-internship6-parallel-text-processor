import os
import re
import json
import time
import sqlite3
 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
 
# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Crisis Communication Monitor",
    layout="wide",
)
 
st.title("Parallel Text Handling Processor")
st.caption("Disaster & Crisis Communication Monitor — Infosys Springboard Project")
 
# ── Load JSON insights ────────────────────────────────────────────────────────
@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None
 
tweet_data = load_json("data/tweet_insights.json")
wa_data    = load_json("data/whatsapp_insights.json")
 
# ── Load CSV outputs ──────────────────────────────────────────────────────────
@st.cache_data
def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None
 
tweet_csv = load_csv("output/tweet_results.csv")
wa_csv    = load_csv("output/whatsapp_results.csv")
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — INPUT OPTIONS + REAL-TIME CLEANING PREVIEW
# ═══════════════════════════════════════════════════════════════════════════════
st.sidebar.title("📂 Input Options")
 
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
manual_input  = st.sidebar.text_area("Or Enter Text Manually")
analyze_btn   = st.sidebar.button("Analyze")
 
# ── Real-Time Cleaning Preview ─────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.subheader("Real-Time Cleaning Preview")
clean_text_input = st.sidebar.text_input("Enter text to see cleaning steps")
 
if clean_text_input:
    try:
        from nltk.corpus import stopwords
        STOP_WORDS = set(stopwords.words('english'))
    except Exception:
        STOP_WORDS = set()
 
    # Step 1 — Original
    st.sidebar.write("**Step 1: Original Text**")
    st.sidebar.code(clean_text_input)
 
    # Step 2 — Remove URLs & Mentions
    step2 = re.sub(r'http\S+|www\S+', '', clean_text_input)
    step2 = re.sub(r'@\w+', '', step2)
    st.sidebar.write("**Step 2: Remove URLs & Mentions**")
    st.sidebar.code(step2.strip())
 
    # Step 3 — Remove Special Chars
    step3 = re.sub(r'#', '', step2)
    step3 = re.sub(r'[^a-zA-Z\s]', '', step3)
    st.sidebar.write("**Step 3: Remove Special Chars**")
    st.sidebar.code(step3.strip())
 
    # Step 4 — Lowercase
    step4 = step3.lower().strip()
    st.sidebar.write("**Step 4: Lowercase**")
    st.sidebar.code(step4)
 
    # Step 5 — Remove Stopwords
    words = step4.split()
    cleaned_words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    step5 = " ".join(cleaned_words)
    st.sidebar.write("**Step 5: Remove Stopwords**")
    st.sidebar.code(step5)
 
    # Cleaning Summary
    st.sidebar.write("**📊 Cleaning Summary**")
    original_len = len(clean_text_input.split())
    cleaned_len  = len(cleaned_words)
    st.sidebar.metric("Words Removed", original_len - cleaned_len)
    st.sidebar.metric("Final Words",   cleaned_len)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# REAL-TIME PROCESSING — uses project modules directly
# ═══════════════════════════════════════════════════════════════════════════════
from preprocessing import clean_text_realtime
from processor import process_single_realtime
from rule_engine import apply_rules_single, detect_alert_level
 
 
def detect_text_column(df: pd.DataFrame) -> str:
    preferred = ["text", "tweet", "message", "content", "msg", "body"]
    lower_cols = {c.lower().strip(): c for c in df.columns}
    for name in preferred:
        if name in lower_cols:
            return lower_cols[name]
    str_cols = df.select_dtypes(include="object").columns.tolist()
    if str_cols:
        return max(str_cols, key=lambda c: df[c].dropna().astype(str).str.len().mean())
    return df.columns[0]
 
 
def extract_location(text: str) -> str:
    try:
        words = str(text).split()
        for i, w in enumerate(words):
            if w.lower() in ["near", "in", "at"] and i + 1 < len(words):
                return words[i + 1].strip(".,")
    except Exception:
        pass
    return "Unknown"
 
 
# ── Run real-time analysis when button clicked ─────────────────────────────
df_results   = None
detected_col = None
 
if uploaded_file and analyze_btn:
    try:
        df_upload    = pd.read_csv(uploaded_file)
        detected_col = detect_text_column(df_upload)
        data         = df_upload[detected_col].dropna().astype(str).tolist()
 
        if not data:
            st.sidebar.warning("No text rows found in the selected column.")
        else:
            with st.spinner(f"Analysing {len(data):,} messages from column '{detected_col}'…"):
                time.sleep(0.5)
                rows = []
                for text in data:
                    cleaned = clean_text_realtime(text)
                    proc    = process_single_realtime(cleaned)
                    rules   = apply_rules_single(cleaned)
                    alert   = detect_alert_level(rules)
                    rows.append({
                        "text":      text,
                        "alert":     alert,
                        "sentiment": round(proc["sentiment"], 3),
                        "keywords":  ", ".join(proc["keywords"]),
                        "location":  extract_location(text),
                    })
                df_results = pd.DataFrame(rows)
 
    except Exception as e:
        st.error(f"Error processing CSV: {e}")
 
elif uploaded_file and not analyze_btn:
    st.sidebar.info("Click **Analyze** to process the uploaded file.")
 
 

# TABS

tab0, tab1, tab2, tab3 = st.tabs([
    "Real-Time Analysis",
    "Tweets",
    "WhatsApp",
    "Rule Engine",
])
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# TAB 0 — REAL-TIME ANALYSIS (NEW)
# ═══════════════════════════════════════════════════════════════════════════════
with tab0:
    if df_results is not None and not df_results.empty:
 
        st.success(f"Processed **{len(df_results):,}** messages from column `{detected_col}`")
 
        col1, col2, col3, col4 = st.columns(4)
 
        high_count   = int((df_results["alert"] == "HIGH 🚨").sum())
        medium_count = int((df_results["alert"] == "MEDIUM ⚠️").sum())
        low_count    = int((df_results["alert"] == "LOW ✅").sum())
        avg_sent     = round(df_results["sentiment"].mean(), 3)
 
        col1.metric(" Total Messages",  len(df_results))
        col2.metric(" HIGH Alerts",     high_count)
        col3.metric(" MEDIUM Alerts",   medium_count)
        col4.metric(" Avg Sentiment",   avg_sent)
 
        st.divider()
 
        st.subheader(" Alert Level Distribution")
        st.bar_chart(df_results["alert"].value_counts())
 
        st.subheader(" Sentiment Distribution")
        fig_sent, ax_sent = plt.subplots(figsize=(8, 3))
        ax_sent.hist(df_results["sentiment"], bins=30)
        st.pyplot(fig_sent)
 
        all_words = " ".join(df_results["keywords"].dropna())
        if all_words.strip():
            st.subheader(" Keyword Word Cloud")
            wc = WordCloud(width=700, height=300,
                           background_color="white").generate(all_words)
            fig_wc, ax_wc = plt.subplots(figsize=(10, 4))
            ax_wc.imshow(wc)
            ax_wc.axis("off")
            st.pyplot(fig_wc)
 
        st.subheader(" Detailed Results")
        st.dataframe(df_results, use_container_width=True)
 
    else:
        st.info(" Use the sidebar to **Upload CSV** or **Enter Text**, then click ** Analyze** to see real-time results here.")
        st.markdown("""
        **How this works:**
        - Upload any CSV file — the first column is used as text input
        - Or type/paste messages directly in the sidebar text box
        - Each message is cleaned, tokenised, sentiment-scored, and classified by alert level
        - **HIGH ** = distress signals detected &nbsp; | &nbsp; **MEDIUM ** = disaster/resource keywords &nbsp; | &nbsp; **LOW ** = no crisis keywords
        """)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TWEETS
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    if tweet_data is None:
        st.warning("Run `main.py` first to generate outputs.")
    else:
        perf = tweet_data.get("performance", {})
 
        st.subheader(" Processing Performance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sequential Time", f"{perf.get('sequential_time', '—')}s")
        c2.metric("Parallel Time",   f"{perf.get('parallel_time', '—')}s")
        c3.metric("Speedup",         f"{perf.get('speedup', '—')}x")
        c4.metric("CPU Cores Used",  perf.get('num_cores', '—'))
 
        st.divider()
        col1, col2 = st.columns(2)
 
        with col1:
            st.subheader(" Top Keywords")
            kw = tweet_data.get("top_keywords", {})
            if kw:
                df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"]).head(20)
                st.bar_chart(df_kw.set_index("Word"))
 
        with col2:
            st.subheader(" Word Cloud")
            if kw:
                wc = WordCloud(width=600, height=300, background_color="white",
                               colormap="Reds").generate_from_frequencies(kw)
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
                plt.close(fig)
 
        st.subheader(" Average Sentiment")
        sentiment = tweet_data.get("avg_sentiment", 0)
        col_a, col_b = st.columns([1, 3])
        with col_a:
            label = " Positive" if sentiment > 0.05 else (" Negative" if sentiment < -0.05 else " Neutral")
            st.metric(label, f"{sentiment:.4f}")
        with col_b:
            st.progress(min(max((sentiment + 1) / 2, 0), 1))
 
        st.divider()
        st.subheader(" Rule Engine — Tweet Analysis")
        rc1, rc2 = st.columns(2)
        with rc1:
            if os.path.exists("output/tweet_barchart.png"):
                st.image("output/tweet_barchart.png", caption="Total Matches per Rule")
        with rc2:
            if os.path.exists("output/tweet_linechart.png"):
                st.image("output/tweet_linechart.png", caption="Keyword Signal per Chunk")
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — WHATSAPP
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    if wa_data is None:
        st.warning("Run `main.py` first to generate outputs.")
    else:
        perf = wa_data.get("performance", {})
 
        st.subheader(" Processing Performance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sequential Time", f"{perf.get('sequential_time', '—')}s")
        c2.metric("Parallel Time",   f"{perf.get('parallel_time', '—')}s")
        c3.metric("Speedup",         f"{perf.get('speedup', '—')}x")
        c4.metric("CPU Cores Used",  perf.get('num_cores', '—'))
 
        st.divider()
        col1, col2 = st.columns(2)
 
        with col1:
            st.subheader(" Top Keywords")
            kw = wa_data.get("top_keywords", {})
            if kw:
                df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"]).head(20)
                st.bar_chart(df_kw.set_index("Word"))
 
        with col2:
            st.subheader(" Word Cloud")
            if kw:
                wc = WordCloud(width=600, height=300, background_color="white",
                               colormap="Blues").generate_from_frequencies(kw)
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
                plt.close(fig)
 
        st.subheader("👥 Most Active Senders")
        senders = wa_data.get("top_senders", {})
        if senders:
            df_s = pd.DataFrame(list(senders.items()), columns=["Sender", "Messages"])
            st.bar_chart(df_s.set_index("Sender"))
 
        st.subheader(" Average Sentiment")
        sentiment = wa_data.get("avg_sentiment", 0)
        col_a, col_b = st.columns([1, 3])
        with col_a:
            label = " Positive" if sentiment > 0.05 else (" Negative" if sentiment < -0.05 else " Neutral")
            st.metric(label, f"{sentiment:.4f}")
        with col_b:
            st.progress(min(max((sentiment + 1) / 2, 0), 1))
 
        st.divider()
        st.subheader("🔍 Rule Engine — WhatsApp Analysis")
        rc1, rc2 = st.columns(2)
        with rc1:
            if os.path.exists("output/whatsapp_barchart.png"):
                st.image("output/whatsapp_barchart.png", caption="Total Matches per Rule")
        with rc2:
            if os.path.exists("output/whatsapp_linechart.png"):
                st.image("output/whatsapp_linechart.png", caption="Keyword Signal per Chunk")
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RULE ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader(" Regex Rule Engine Outputs")
    st.markdown("""
    The rule engine applies **7 predefined regex pattern categories** to every text chunk
    processed in parallel. Results are saved to CSV and SQLite.
    """)
 
    rules_info = {
        "distress_signals":  r"\b(help|trapped|rescue|sos|urgent|missing|survivor|stranded|emergency|mayday)\b",
        "disaster_types":    r"\b(flood|earthquake|fire|cyclone|tsunami|hurricane|tornado|landslide|wildfire|drought)\b",
        "locations":         r"\b(road|river|village|colony|district|bridge|building|hospital|school|shelter)\b",
        "resources":         r"\b(food|water|boat|ambulance|shelter|medicine|clothes|blanket|supply|aid)\b",
        "sentiment_words":   r"\b(danger|dangerous|safe|safety|critical|improving|severe|deadly|devastating|hopeful)\b",
        "action_keywords":   r"\b(evacuate|evacuated|deployed|rescue|relief|respond|alert|warn|coordinate)\b",
        "infrastructure":    r"\b(power|electricity|network|communication|highway|airport|port|dam|pipeline|grid)\b",
    }
    df_rules = pd.DataFrame(list(rules_info.items()), columns=["Rule", "Pattern"])
    st.dataframe(df_rules, use_container_width=True)
 
    st.divider()
    col1, col2 = st.columns(2)
 
    with col1:
        st.subheader(" Tweet Results CSV")
        if tweet_csv is not None:
            st.dataframe(tweet_csv.head(100), use_container_width=True)
            st.caption(f"{len(tweet_csv):,} rows total — showing first 100")
        else:
            st.info("Run `main.py` to generate output/tweet_results.csv")
 
    with col2:
        st.subheader(" WhatsApp Results CSV")
        if wa_csv is not None:
            st.dataframe(wa_csv.head(100), use_container_width=True)
            st.caption(f"{len(wa_csv):,} rows total — showing first 100")
        else:
            st.info("Run `main.py` to generate output/whatsapp_results.csv")
 
    st.divider()
    st.subheader(" SQLite Database — results.db")
    db_path = "output/results.db"
    if os.path.exists(db_path):
        conn   = sqlite3.connect(db_path)
        tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
        st.write(f"Tables in database: **{', '.join(tables['name'].tolist())}**")
        for tbl in tables["name"].tolist():
            count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {tbl}", conn).iloc[0, 0]
            st.write(f"  • `{tbl}` — {count:,} rows")
        conn.close()
        st.success(f"Database is live at: {db_path}")
    else:
        st.info("Run `main.py` to generate output/results.db")
 
 
# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "Parallel Text Handling Processor — Infosys Springboard | "
    "Python · multiprocessing · ProcessPoolExecutor · NLTK · TextBlob · SQLite · Streamlit"
)