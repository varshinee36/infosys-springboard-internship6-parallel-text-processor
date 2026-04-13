import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import time

from preprocessing import clean_text_realtime
from processor import process_single_realtime
from rule_engine import apply_rules_single, detect_alert_level

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
st.set_page_config(layout="wide", page_title="Crisis Monitor")

st.title("🚨 Disaster Monitoring System")

# ─────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────
if "df_results" not in st.session_state:
    st.session_state.df_results = None

if "alert_filter" not in st.session_state:
    st.session_state.alert_filter = "All"

# ─────────────────────────────
# SIDEBAR
# ─────────────────────────────
st.sidebar.title("📂 Input Options")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
manual_input = st.sidebar.text_area("Or Enter Text", height=150)
analyze_btn = st.sidebar.button("🚀 Analyze")

# ─────────────────────────────
# LOCATION
# ─────────────────────────────
def extract_location(text):
    words = text.split()
    for i, w in enumerate(words):
        if w.lower() in ["near", "in", "at"]:
            if i + 1 < len(words):
                return words[i + 1]
    return "Unknown"

# ─────────────────────────────
# LOAD DATA
# ─────────────────────────────
data = []

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    data = df.iloc[:, 0].dropna().tolist()

elif manual_input:
    data = manual_input.split("\n")

# ─────────────────────────────
# PROCESS
# ─────────────────────────────
if analyze_btn and data:

    with st.spinner("Analyzing..."):
        time.sleep(1)

        results = []

        for text in data:
            cleaned = clean_text_realtime(text)
            proc = process_single_realtime(cleaned)
            rules = apply_rules_single(cleaned)
            alert = detect_alert_level(rules)

            location = extract_location(text)

            results.append({
                "text": text,
                "alert": alert,
                "sentiment": proc["sentiment"],
                "keywords": ", ".join(proc["keywords"]),
                "location": location
            })

        st.session_state.df_results = pd.DataFrame(results)

# ─────────────────────────────
# MAIN
# ─────────────────────────────
df_results = st.session_state.df_results

if df_results is not None:

    alert_counts = df_results["alert"].value_counts()
    all_words = " ".join(df_results["keywords"])
    word_freq = pd.Series(all_words.split()).value_counts()

    # ✅ CORRECT RADIO (NO RESET)
    section = st.radio(
        "Navigation",
        ["📊 Summary", "🚨 Alerts", "🔍 Keywords", "🧠 Insights"],
        horizontal=True,
        key="nav_radio"   # 🔥 THIS FIXES RESET
    )

    # ───────── SUMMARY ─────────
    if section == "📊 Summary":

        st.subheader("📊 Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("Messages", len(df_results))
        col2.metric("Avg Sentiment", round(df_results["sentiment"].mean(), 3))
        col3.metric("High Alerts", alert_counts.get("HIGH 🚨", 0))

    # ───────── ALERTS ─────────
    elif section == "🚨 Alerts":

        st.subheader("🚨 Alert Distribution")

        st.bar_chart(alert_counts)

        fig, ax = plt.subplots(figsize=(2,2))
        labels = [l.split()[0] for l in alert_counts.index]

        ax.pie(alert_counts, labels=labels, autopct='%1.1f%%', textprops={'fontsize':7})
        st.pyplot(fig, use_container_width=False)

        st.markdown("### 🔍 Filter Messages")

        selected = st.selectbox(
            "Select Alert Type",
            ["All"] + list(df_results["alert"].unique()),
            key="alert_filter"   # 🔥 persists value
        )

        if selected != "All":
            filtered = df_results[df_results["alert"] == selected]
        else:
            filtered = df_results

        st.dataframe(filtered)

    # ───────── KEYWORDS ─────────
    elif section == "🔍 Keywords":

        st.subheader("🔍 Keyword Analysis")

        # Horizontal bar chart
        st.bar_chart(word_freq.head(10))

        # WordCloud
        wc = WordCloud(width=500, height=250).generate(all_words)

        fig, ax = plt.subplots(figsize=(6,3))
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)

        # Alert-driving keywords
        st.markdown("### 🚨 Alert Driving Keywords")

        high_alert_text = df_results[df_results["alert"].str.contains("HIGH")]

        if not high_alert_text.empty:
            high_words = " ".join(high_alert_text["keywords"])
            high_freq = pd.Series(high_words.split()).value_counts()
            st.write(high_freq.head(5))

    # ───────── INSIGHTS ─────────
    elif section == "🧠 Insights":

        st.subheader("🧠 Insights")

        st.subheader("🚨 Key Findings")

        for _, row in df_results.iterrows():
            if "HIGH" in row["alert"]:
                st.error(f"🚨 CRITICAL: {row['location']} → Immediate action needed")
            elif "MEDIUM" in row["alert"]:
                st.warning(f"⚠️ ALERT: {row['location']} → Monitor situation")

        st.markdown("---")

        st.subheader("📈 Alert Trend")
        st.line_chart(alert_counts)

else:
    st.info("Upload CSV or enter text and click Analyze")