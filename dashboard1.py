import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time
import re  # ✅ added

# Real-time imports
from preprocessing import clean_text, clean_text_realtime
from processor import process_single_realtime
from rule_engine import apply_rules_single, detect_alert_level

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(page_title="Crisis Monitor", layout="wide")
st.title("🚨 Disaster Monitoring System")

# ─────────────────────────────
# SIDEBAR — CSV UPLOAD ONLY
# ─────────────────────────────
st.sidebar.title("📂 Input Options")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
analyze_btn   = st.sidebar.button("🚀 Analyze")

# ─────────────────────────────
# 🧹 REAL-TIME CLEANING PREVIEW (ADDED)
# ─────────────────────────────
st.sidebar.markdown("---")
st.sidebar.subheader("🧹 Real-Time Cleaning Preview")

clean_text_input = st.sidebar.text_input("Enter text to preview cleaning")

if clean_text_input:
    try:
        from nltk.corpus import stopwords
        STOP_WORDS = set(stopwords.words('english'))
    except:
        STOP_WORDS = set()

    # Step 1 — Original
    st.sidebar.write("**Step 1: Original Text**")
    st.sidebar.code(clean_text_input)

    # Step 2 — Remove URLs & Mentions
    step2 = re.sub(r'http\S+|www\S+', '', clean_text_input)
    step2 = re.sub(r'@\w+', '', step2)
    st.sidebar.write("**Step 2: Remove URLs & Mentions**")
    st.sidebar.code(step2.strip())

    # Step 3 — Remove Special Characters
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

    # Summary
    st.sidebar.write("**📊 Cleaning Summary**")
    st.sidebar.metric("Words Removed", len(words) - len(cleaned_words))
    st.sidebar.metric("Final Words", len(cleaned_words))

# ─────────────────────────────
# LOAD JSON (BATCH DATA)
# ─────────────────────────────
@st.cache_data
def load_json(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

tweet_data = load_json("data/tweet_insights.json")
wa_data    = load_json("data/whatsapp_insights.json")

# ─────────────────────────────
# HELPERS
# ─────────────────────────────
def extract_location(text):
    words = text.split()
    for i, w in enumerate(words):
        if w.lower() in ["near", "in", "at"]:
            if i + 1 < len(words):
                return words[i + 1].strip(".,")
    return "Unknown"


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

# ─────────────────────────────
# REAL-TIME PROCESSING
# ─────────────────────────────
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

                results = []
                for text in data:
                    cleaned = clean_text_realtime(text)
                    proc    = process_single_realtime(cleaned)
                    rules   = apply_rules_single(cleaned)
                    alert   = detect_alert_level(rules)

                    results.append({
                        "text":      text,
                        "alert":     alert,
                        "sentiment": round(proc["sentiment"], 3),
                        "keywords":  ", ".join(proc["keywords"]),
                        "location":  extract_location(text),
                    })

                df_results = pd.DataFrame(results)

    except Exception as e:
        st.error(f"Error processing CSV: {e}")

elif uploaded_file and not analyze_btn:
    st.sidebar.info("Click **🚀 Analyze** to process the uploaded file.")

# ─────────────────────────────
# TABS
# ─────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["📡 Real-Time Analysis", "📊 Analytics", "🔍 Rule Engine", "⚙️ Pipeline"]
)

# ═══════════════════════════════
# TAB 1 — REAL-TIME ANALYSIS
# ═══════════════════════════════
with tab1:
    if df_results is not None and not df_results.empty:

        st.success(f"Processed **{len(df_results):,}** messages from column `{detected_col}`")

        col1, col2, col3, col4 = st.columns(4)

        high_count   = int((df_results["alert"] == "HIGH 🚨").sum())
        medium_count = int((df_results["alert"] == "MEDIUM ⚠️").sum())
        low_count    = int((df_results["alert"] == "LOW ✅").sum())
        avg_sent     = round(df_results["sentiment"].mean(), 3)

        col1.metric("📨 Total Messages",  len(df_results))
        col2.metric("🚨 HIGH Alerts",     high_count)
        col3.metric("⚠️ MEDIUM Alerts",   medium_count)
        col4.metric("📈 Avg Sentiment",   avg_sent)

        st.divider()

        st.subheader("🔔 Alert Level Distribution")
        st.bar_chart(df_results["alert"].value_counts())

        st.subheader("📊 Sentiment Distribution")
        fig_sent, ax_sent = plt.subplots(figsize=(8, 3))
        ax_sent.hist(df_results["sentiment"], bins=30)
        st.pyplot(fig_sent)

        all_words = " ".join(df_results["keywords"].dropna())
        if all_words.strip():
            st.subheader("☁️ Keyword Word Cloud")
            wc = WordCloud(width=700, height=300,
                           background_color="white").generate(all_words)
            fig_wc, ax_wc = plt.subplots(figsize=(10, 4))
            ax_wc.imshow(wc)
            ax_wc.axis("off")
            st.pyplot(fig_wc)

        st.subheader("📋 Detailed Results")
        st.dataframe(df_results, use_container_width=True)

    else:
        st.info("⬅️ Upload a CSV and click **🚀 Analyze** to see results here.")

# ═══════════════════════════════
# TAB 2 — ANALYTICS
# ═══════════════════════════════
with tab2:
    if tweet_data:
        st.subheader("📊 Top Keywords — Tweets")
        kw = tweet_data.get("top_keywords", {})
        if kw:
            df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"])
            st.bar_chart(df_kw.set_index("Word"))

    if wa_data:
        st.subheader("📊 Top Keywords — WhatsApp")
        kw_wa = wa_data.get("top_keywords", {})
        if kw_wa:
            df_kw_wa = pd.DataFrame(list(kw_wa.items()), columns=["Word", "Count"])
            st.bar_chart(df_kw_wa.set_index("Word"))

# ═══════════════════════════════
# TAB 3 — RULE ENGINE
# ═══════════════════════════════
with tab3:
    st.subheader("🔍 Rule Engine — Processed CSV Results")

    tweet_csv = "output/tweet_results.csv"
    wa_csv    = "output/whatsapp_results.csv"

    if os.path.exists(tweet_csv):
        st.dataframe(pd.read_csv(tweet_csv).head(50))
    elif os.path.exists(wa_csv):
        st.dataframe(pd.read_csv(wa_csv).head(50))
    else:
        st.info("No processed CSVs found.")

# ═══════════════════════════════
# TAB 4 — PIPELINE
# ═══════════════════════════════
with tab4:
    st.subheader("⚙️ System Pipeline")
    st.code("Pipeline unchanged")