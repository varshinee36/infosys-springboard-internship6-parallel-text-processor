# # import streamlit as st
# # import pandas as pd
# # import json
# # import matplotlib.pyplot as plt
# # from wordcloud import WordCloud

# # st.set_page_config(
# #     page_title="Disaster Communication Monitor",
# #     page_icon="🚨",
# #     layout="wide"
# # )

# # # ── TITLE ──
# # st.title("Parallel Text Handling Processor")
# # st.markdown("**Disaster & Crisis Communication Monitor** — analyzing tweets and WhatsApp messages in parallel")
# # st.divider()

# # # ── HOW IT WORKS SECTION ──
# # st.subheader("How This System Works")
# # col1, col2, col3, col4, col5 = st.columns(5)
# # with col1:
# #     st.info("**Step 1**\nRaw tweets + WhatsApp messages loaded from datasets")
# # with col2:
# #     st.info("**Step 2**\nText cleaned — URLs, mentions, symbols removed")
# # with col3:
# #     st.info("**Step 3**\nData split into chunks — one per CPU core")
# # with col4:
# #     st.info("**Step 4**\nAll cores analyse simultaneously in parallel")
# # with col5:
# #     st.info("**Step 5**\nResults merged and displayed here")

# # st.divider()

# # # ── LOAD JSON FILES ──
# # with open("data/tweet_insights.json", "r") as f:
# #     tweet_data = json.load(f)

# # with open("data/whatsapp_insights.json", "r") as f:
# #     whatsapp_data = json.load(f)

# # # ── PERFORMANCE METRICS SECTION ──
# # st.subheader("Parallel Processing Performance")
# # st.markdown("This system processed **76,295 texts** across two datasets using parallel computing:")

# # perf = tweet_data['performance']

# # col1, col2, col3, col4 = st.columns(4)
# # with col1:
# #     st.metric(
# #         label="Sequential Time",
# #         value=f"{perf['sequential_time']}s",
# #         delta="One core only"
# #     )
# # with col2:
# #     st.metric(
# #         label="Parallel Time",
# #         value=f"{perf['parallel_time']}s",
# #         delta="All cores working"
# #     )
# # with col3:
# #     st.metric(
# #         label="Speedup Achieved",
# #         value=f"{perf['speedup']}x faster",
# #         delta="Parallel vs Sequential"
# #     )
# # with col4:
# #     st.metric(
# #         label="CPU Cores Used",
# #         value=f"{perf['num_cores']} cores",
# #         delta="Simultaneous processing"
# #     )

# # # Simple speedup explanation
# # st.markdown(f"""
# # > **What this means:** Instead of one CPU core processing all 76,295 texts one by one 
# # > (taking **{perf['sequential_time']}s**), we split the work across **{perf['num_cores']} cores** 
# # > working simultaneously — finishing in just **{perf['parallel_time']}s**. 
# # > That is **{perf['speedup']}x faster** — critical when disaster response needs real-time insights.
# # """)

# # st.divider()

# # # ── TABS ──
# # tab1, tab2 = st.tabs(["Tweets Analysis", "WhatsApp Analysis"])

# # # ── TAB 1 — TWEETS ──
# # with tab1:
# #     st.header("Tweet Stream Analysis")
# #     st.markdown(f"Analysing **{tweet_data['total']:,}** disaster-related tweets from 26 global crisis events")
# #     st.caption(f"Processed using {perf['num_cores']} CPU cores in parallel — {perf['parallel_time']}s total processing time")

# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         st.metric(
# #             label="Overall Sentiment",
# #             value=f"{tweet_data['avg_sentiment']:.2f}",
# #             delta="Slightly Negative" if tweet_data['avg_sentiment'] < 0 else "Slightly Positive"
# #         )
# #     with col2:
# #         st.metric(label="Total Tweets Processed", value=f"{tweet_data['total']:,}")
# #     with col3:
# #         st.metric(label="Crisis Events Covered", value="26")

# #     st.subheader("Top Disaster Keywords")
# #     st.caption("Most frequently mentioned words across all 26 crisis events — bigger bar = more mentions")
# #     keywords_df = pd.DataFrame(tweet_data['top_keywords'], columns=['keyword', 'count'])
# #     keywords_df = keywords_df.set_index('keyword')
# #     st.bar_chart(keywords_df)

# #     st.subheader("Word Cloud")
# #     st.caption("Word size = frequency — the bigger the word, the more people mentioned it")
# #     word_freq_dict = dict(tweet_data['top_keywords'])
# #     wc = WordCloud(
# #         width=800, height=400,
# #         background_color='white',
# #         colormap='Reds'
# #     ).generate_from_frequencies(word_freq_dict)
# #     fig, ax = plt.subplots(figsize=(10, 5))
# #     ax.imshow(wc, interpolation='bilinear')
# #     ax.axis('off')
# #     st.pyplot(fig)
# #     plt.close()

# # # ── TAB 2 — WHATSAPP ──
# # with tab2:
# #     st.header("WhatsApp Chat Analysis")
# #     st.markdown(f"Analysing **{whatsapp_data['total']:,}** community messages from disaster response groups")
# #     st.caption(f"Processed using {perf['num_cores']} CPU cores in parallel — ground level crisis communication")

# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         st.metric(
# #             label="Overall Sentiment",
# #             value=f"{whatsapp_data['avg_sentiment']:.2f}",
# #             delta="Slightly Negative" if whatsapp_data['avg_sentiment'] < 0 else "Slightly Positive"
# #         )
# #     with col2:
# #         st.metric(label="Total Messages Processed", value=f"{whatsapp_data['total']:,}")
# #     with col3:
# #         st.metric(label="Unique Senders", value="4")

# #     st.subheader("Top Keywords in Messages")
# #     st.caption("Most urgent topics from ground level WhatsApp communication")
# #     keywords_df = pd.DataFrame(whatsapp_data['top_keywords'], columns=['keyword', 'count'])
# #     keywords_df = keywords_df.set_index('keyword')
# #     st.bar_chart(keywords_df)

# #     st.subheader("Most Active Senders")
# #     st.caption("Community members contributing most to disaster communication")
# #     senders_df = pd.DataFrame(whatsapp_data['top_senders'], columns=['sender', 'messages'])
# #     senders_df = senders_df.set_index('sender')
# #     st.bar_chart(senders_df)

# #     st.subheader("Word Cloud")
# #     st.caption("Word size = frequency — dominant ground level concerns")
# #     word_freq_dict = dict(whatsapp_data['top_keywords'])
# #     wc = WordCloud(
# #         width=800, height=400,
# #         background_color='white',
# #         colormap='Blues'
# #     ).generate_from_frequencies(word_freq_dict)
# #     fig, ax = plt.subplots(figsize=(10, 5))
# #     ax.imshow(wc, interpolation='bilinear')
# #     ax.axis('off')
# #     st.pyplot(fig)
# #     plt.close()

# # # ── FOOTER ──
# # st.divider()
# # st.caption("Parallel Text Handling Processor — Infosys Springboard Project | Built with Python, multiprocessing, NLTK, TextBlob, Streamlit")    



# # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

# # import streamlit as st
# # import pandas as pd
# # import json
# # import matplotlib.pyplot as plt
# # from wordcloud import WordCloud

# # st.set_page_config(
# #     page_title="Disaster Crisis Monitor",
# #     page_icon="🚨",
# #     layout="wide"
# # )

# # st.title("Parallel Text Handling Processor")
# # st.markdown("**Disaster & Crisis Communication Monitor** — Rule Engine + Parallel Processing + SQLite Storage")
# # st.divider()

# # # ── HOW IT WORKS ──
# # st.subheader("System Pipeline")
# # cols = st.columns(6)
# # steps = [
# #     ("1", "Load Data", "Tweets + WhatsApp datasets"),
# #     ("2", "Clean Text", "Remove URLs, mentions, symbols"),
# #     ("3", "Chunk", "Split into CPU-core chunks"),
# #     ("4", "Parallel", "ProcessPoolExecutor + as_completed"),
# #     ("5", "Rule Engine", "7 crisis regex categories per text"),
# #     ("6", "SQLite", "Results stored in crisis_insights.db"),
# # ]
# # for col, (num, title, desc) in zip(cols, steps):
# #     with col:
# #         st.info(f"**Step {num}: {title}**\n\n{desc}")

# # st.divider()

# # # ── LOAD JSON ──
# # with open("data/tweet_insights.json", "r") as f:
# #     tweet_data = json.load(f)

# # with open("data/whatsapp_insights.json", "r") as f:
# #     whatsapp_data = json.load(f)

# # perf = tweet_data['performance']

# # # ── PERFORMANCE METRICS ──
# # st.subheader("Parallel Processing Performance")
# # c1, c2, c3, c4 = st.columns(4)
# # with c1:
# #     st.metric("Sequential Time", f"{perf['sequential_time']}s", "Single core")
# # with c2:
# #     st.metric("Parallel Time",   f"{perf['parallel_time']}s",   "All cores")
# # with c3:
# #     st.metric("Speedup",         f"{perf['speedup']}x",          "Faster")
# # with c4:
# #     st.metric("CPU Cores",       f"{perf['num_cores']}",          "Workers")

# # st.markdown(f"""
# # > **ProcessPoolExecutor** with `as_completed()` splits {tweet_data['total']:,} tweets + {whatsapp_data['total']:,} WhatsApp messages  
# # > across **{perf['num_cores']} CPU cores**, reducing processing from **{perf['sequential_time']}s → {perf['parallel_time']}s** ({perf['speedup']}x speedup).  
# # > Results saved to **SQLite database** (`crisis_insights.db`) for persistence.
# # """)

# # st.divider()

# # # ── TABS ──
# # tab1, tab2, tab3 = st.tabs(["Tweet Analysis", "WhatsApp Analysis", "Crisis Rule Engine"])

# # # ══════════════════════════════════════════════
# # # TAB 1 — TWEETS
# # # ══════════════════════════════════════════════
# # with tab1:
# #     st.header("Tweet Stream Analysis")
# #     st.markdown(f"**{tweet_data['total']:,}** disaster tweets from 26 global crisis events")

# #     c1, c2, c3 = st.columns(3)
# #     with c1:
# #         sentiment_label = "Negative" if tweet_data['avg_sentiment'] < 0 else "Positive"
# #         st.metric("Overall Sentiment", f"{tweet_data['avg_sentiment']:.3f}", sentiment_label)
# #     with c2:
# #         st.metric("Tweets Processed", f"{tweet_data['total']:,}")
# #     with c3:
# #         st.metric("Crisis Events", "26")

# #     # Crisis category breakdown
# #     st.subheader("Crisis Category Distribution (Rule Engine)")
# #     st.caption("Each tweet classified by dominant crisis type using regex rule patterns")
# #     crisis_df = pd.DataFrame(
# #         list(tweet_data['crisis_distribution'].items()),
# #         columns=['Crisis Type', 'Count']
# #     ).set_index('Crisis Type').sort_values('Count', ascending=False)
# #     st.bar_chart(crisis_df)

# #     # Chunk intensity line chart (matches reference project output)
# #     st.subheader("Processing Intensity per Chunk")
# #     st.caption("Texts processed per CPU worker chunk — shows parallel workload distribution")
# #     intensity_df = pd.DataFrame(
# #         list(tweet_data['chunk_intensity'].items()),
# #         columns=['Chunk', 'Texts Processed']
# #     ).set_index('Chunk')
# #     st.line_chart(intensity_df)

# #     # Top keywords bar chart
# #     st.subheader("Top Disaster Keywords")
# #     kw_df = pd.DataFrame(tweet_data['top_keywords'], columns=['keyword', 'count']).set_index('keyword')
# #     st.bar_chart(kw_df)

# #     # Word cloud
# #     st.subheader("Word Cloud")
# #     wc = WordCloud(width=800, height=400, background_color='white', colormap='Reds'
# #                    ).generate_from_frequencies(dict(tweet_data['top_keywords']))
# #     fig, ax = plt.subplots(figsize=(10, 4))
# #     ax.imshow(wc, interpolation='bilinear')
# #     ax.axis('off')
# #     st.pyplot(fig)
# #     plt.close()

# # # ══════════════════════════════════════════════
# # # TAB 2 — WHATSAPP
# # # ══════════════════════════════════════════════
# # with tab2:
# #     st.header("WhatsApp Chat Analysis")
# #     st.markdown(f"**{whatsapp_data['total']:,}** community messages from disaster response groups")

# #     c1, c2, c3 = st.columns(3)
# #     with c1:
# #         sentiment_label = "Negative" if whatsapp_data['avg_sentiment'] < 0 else "Positive"
# #         st.metric("Overall Sentiment", f"{whatsapp_data['avg_sentiment']:.3f}", sentiment_label)
# #     with c2:
# #         st.metric("Messages Processed", f"{whatsapp_data['total']:,}")
# #     with c3:
# #         st.metric("Unique Senders", str(len(whatsapp_data.get('top_senders', []))))

# #     # Crisis distribution
# #     st.subheader("Crisis Category Distribution")
# #     st.caption("Rule engine classification of ground-level WhatsApp messages")
# #     crisis_df = pd.DataFrame(
# #         list(whatsapp_data['crisis_distribution'].items()),
# #         columns=['Crisis Type', 'Count']
# #     ).set_index('Crisis Type').sort_values('Count', ascending=False)
# #     st.bar_chart(crisis_df)

# #     # Chunk intensity
# #     st.subheader("Processing Intensity per Chunk")
# #     intensity_df = pd.DataFrame(
# #         list(whatsapp_data['chunk_intensity'].items()),
# #         columns=['Chunk', 'Texts Processed']
# #     ).set_index('Chunk')
# #     st.line_chart(intensity_df)

# #     # Keywords
# #     st.subheader("Top Keywords in Messages")
# #     kw_df = pd.DataFrame(whatsapp_data['top_keywords'], columns=['keyword', 'count']).set_index('keyword')
# #     st.bar_chart(kw_df)

# #     # Senders
# #     if whatsapp_data.get('top_senders'):
# #         st.subheader("Most Active Senders")
# #         senders_df = pd.DataFrame(whatsapp_data['top_senders'], columns=['sender', 'messages']).set_index('sender')
# #         st.bar_chart(senders_df)

# #     # Word cloud
# #     st.subheader("Word Cloud")
# #     wc = WordCloud(width=800, height=400, background_color='white', colormap='Blues'
# #                    ).generate_from_frequencies(dict(whatsapp_data['top_keywords']))
# #     fig, ax = plt.subplots(figsize=(10, 4))
# #     ax.imshow(wc, interpolation='bilinear')
# #     ax.axis('off')
# #     st.pyplot(fig)
# #     plt.close()

# # # ══════════════════════════════════════════════
# # # TAB 3 — RULE ENGINE DEEP DIVE
# # # ══════════════════════════════════════════════
# # with tab3:
# #     st.header("Crisis Rule Engine Analysis")
# #     st.markdown("""
# #     Every tweet and WhatsApp message is analyzed against **7 crisis regex rule categories**.  
# #     This is the same pattern-matching approach used in document analysis systems.  
# #     Results are stored in `crisis_insights.db` (SQLite).
# #     """)

# #     st.subheader("Rule Categories Defined")
# #     rules_info = {
# #         "flood":      "flood, flooding, flooded, inundation, waterlog, river rising...",
# #         "earthquake": "earthquake, quake, tremor, seismic, aftershock, magnitude...",
# #         "wildfire":   "wildfire, fire, blaze, burn, evacuate, smoke, ash, flame...",
# #         "medical":    "injured, hospital, ambulance, casualty, dead, killed, survivor...",
# #         "rescue":     "rescue, help, trapped, sos, urgent, stranded, missing, ndrf...",
# #         "shelter":    "shelter, camp, relief camp, displaced, homeless, food, supply...",
# #         "damage":     "damage, collapsed, broken, infrastructure, road, bridge, power...",
# #     }
# #     for rule, examples in rules_info.items():
# #         st.markdown(f"**`{rule}`** — {examples}")

# #     st.divider()

# #     # Rule totals comparison — tweets vs whatsapp
# #     st.subheader("Rule Match Totals — Tweets vs WhatsApp")
# #     st.caption("Total regex matches per crisis category across both datasets")

# #     tweet_rules = tweet_data.get('rule_totals', {})
# #     wa_rules    = whatsapp_data.get('rule_totals', {})

# #     all_categories = list(set(list(tweet_rules.keys()) + list(wa_rules.keys())))
# #     comparison_df = pd.DataFrame({
# #         'Tweets':    [tweet_rules.get(c, 0) for c in all_categories],
# #         'WhatsApp':  [wa_rules.get(c, 0)    for c in all_categories],
# #     }, index=all_categories)

# #     st.bar_chart(comparison_df)

# #     st.subheader("SQLite Database Info")
# #     st.info("""
# #     All results are stored in `data/crisis_insights.db` with this schema:
    
# #     **Table: crisis_texts**  
# #     `id | label | text | sentiment | crisis_type | flood | earthquake | wildfire | medical | rescue | shelter | damage`
    
# #     Each row = one processed tweet or WhatsApp message with its full rule engine output.
# #     """)

# # # ── FOOTER ──
# # st.divider()
# # st.caption(
# #     "Parallel Text Handling Processor — Infosys Springboard | "
# #     "Python · multiprocessing · ProcessPoolExecutor · NLTK · TextBlob · SQLite · Streamlit"
# # )




# # -----------------------------------------------------------------------------------------------------------------------------------------------------------


# import os
# import json
# import sqlite3
 
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
 
# # ── Page config ───────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Crisis Communication Monitor",
#     layout="wide",
# )
 
# st.title("Parallel Text Handling Processor")
# st.caption("Disaster & Crisis Communication Monitor — Infosys Springboard Project")
 
# # ── Load JSON insights ────────────────────────────────────────────────────────
# @st.cache_data
# def load_json(path):
#     if os.path.exists(path):
#         with open(path) as f:
#             return json.load(f)
#     return None
 
# tweet_data = load_json("data/tweet_insights.json")
# wa_data    = load_json("data/whatsapp_insights.json")
 
# # ── Load CSV outputs ──────────────────────────────────────────────────────────
# @st.cache_data
# def load_csv(path):
#     if os.path.exists(path):
#         return pd.read_csv(path)
#     return None
 
# tweet_csv = load_csv("output/tweet_results.csv")
# wa_csv    = load_csv("output/whatsapp_results.csv")
 
# # ── Tabs ──────────────────────────────────────────────────────────────────────
# tab1, tab2, tab3 = st.tabs(["📡 Tweets", "💬 WhatsApp", "🔍 Rule Engine"])
 
 
# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 1 — TWEETS
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab1:
#     if tweet_data is None:
#         st.warning("Run `main.py` first to generate outputs.")
#     else:
#         perf = tweet_data.get("performance", {})
 
#         # Performance metrics
#         st.subheader("⚡ Processing Performance")
#         c1, c2, c3, c4 = st.columns(4)
#         c1.metric("Sequential Time", f"{perf.get('sequential_time', '—')}s")
#         c2.metric("Parallel Time",   f"{perf.get('parallel_time', '—')}s")
#         c3.metric("Speedup",         f"{perf.get('speedup', '—')}x")
#         c4.metric("CPU Cores Used",  perf.get('num_cores', '—'))
 
#         st.divider()
 
#         col1, col2 = st.columns(2)
 
#         # Top keywords bar chart
#         with col1:
#             st.subheader("📊 Top Keywords")
#             kw = tweet_data.get("top_keywords", {})
#             if kw:
#                 df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"]).head(20)
#                 st.bar_chart(df_kw.set_index("Word"))
 
#         # Word cloud
#         with col2:
#             st.subheader("☁️ Word Cloud")
#             if kw:
#                 wc = WordCloud(width=600, height=300, background_color="white",
#                                colormap="Reds").generate_from_frequencies(kw)
#                 fig, ax = plt.subplots(figsize=(6, 3))
#                 ax.imshow(wc, interpolation="bilinear")
#                 ax.axis("off")
#                 st.pyplot(fig)
#                 plt.close(fig)
 
#         # Sentiment
#         st.subheader("Average Sentiment")
#         sentiment = tweet_data.get("avg_sentiment", 0)
#         col_a, col_b = st.columns([1, 3])
#         with col_a:
#             label = "Positive" if sentiment > 0.05 else ("Negative" if sentiment < -0.05 else "Neutral")
#             st.metric(label, f"{sentiment:.4f}")
#         with col_b:
#             st.progress(min(max((sentiment + 1) / 2, 0), 1))
 
#         # Rule engine charts
#         st.divider()
#         st.subheader("🔍 Rule Engine — Tweet Analysis")
#         rc1, rc2 = st.columns(2)
#         with rc1:
#             if os.path.exists("output/tweet_barchart.png"):
#                 st.image("output/tweet_barchart.png", caption="Total Matches per Rule")
#         with rc2:
#             if os.path.exists("output/tweet_linechart.png"):
#                 st.image("output/tweet_linechart.png", caption="Keyword Signal per Chunk")
 
 
# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 2 — WHATSAPP
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab2:
#     if wa_data is None:
#         st.warning("Run `main.py` first to generate outputs.")
#     else:
#         perf = wa_data.get("performance", {})
 
#         st.subheader("⚡ Processing Performance")
#         c1, c2, c3, c4 = st.columns(4)
#         c1.metric("Sequential Time", f"{perf.get('sequential_time', '—')}s")
#         c2.metric("Parallel Time",   f"{perf.get('parallel_time', '—')}s")
#         c3.metric("Speedup",         f"{perf.get('speedup', '—')}x")
#         c4.metric("CPU Cores Used",  perf.get('num_cores', '—'))
 
#         st.divider()
#         col1, col2 = st.columns(2)
 
#         with col1:
#             st.subheader("📊 Top Keywords")
#             kw = wa_data.get("top_keywords", {})
#             if kw:
#                 df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"]).head(20)
#                 st.bar_chart(df_kw.set_index("Word"))
 
#         with col2:
#             st.subheader("☁️ Word Cloud")
#             if kw:
#                 wc = WordCloud(width=600, height=300, background_color="white",
#                                colormap="Blues").generate_from_frequencies(kw)
#                 fig, ax = plt.subplots(figsize=(6, 3))
#                 ax.imshow(wc, interpolation="bilinear")
#                 ax.axis("off")
#                 st.pyplot(fig)
#                 plt.close(fig)
 
#         # Top senders
#         st.subheader("👥 Most Active Senders")
#         senders = wa_data.get("top_senders", {})
#         if senders:
#             df_s = pd.DataFrame(list(senders.items()), columns=["Sender", "Messages"])
#             st.bar_chart(df_s.set_index("Sender"))
 
#         # Sentiment
#         st.subheader("😐 Average Sentiment")
#         sentiment = wa_data.get("avg_sentiment", 0)
#         col_a, col_b = st.columns([1, 3])
#         with col_a:
#             label = "😊 Positive" if sentiment > 0.05 else ("😢 Negative" if sentiment < -0.05 else "😐 Neutral")
#             st.metric(label, f"{sentiment:.4f}")
#         with col_b:
#             st.progress(min(max((sentiment + 1) / 2, 0), 1))
 
#         # Rule engine charts
#         st.divider()
#         st.subheader("🔍 Rule Engine — WhatsApp Analysis")
#         rc1, rc2 = st.columns(2)
#         with rc1:
#             if os.path.exists("output/whatsapp_barchart.png"):
#                 st.image("output/whatsapp_barchart.png", caption="Total Matches per Rule")
#         with rc2:
#             if os.path.exists("output/whatsapp_linechart.png"):
#                 st.image("output/whatsapp_linechart.png", caption="Keyword Signal per Chunk")
 
 
# # ═══════════════════════════════════════════════════════════════════════════════
# # TAB 3 — RULE ENGINE
# # ═══════════════════════════════════════════════════════════════════════════════
# with tab3:
#     st.subheader("🔍 Regex Rule Engine Outputs")
 
#     st.markdown("""
#     The rule engine applies 7 predefined regex pattern categories to every text chunk
#     processed in parallel. Results are saved to CSV and SQLite.
#     """)
 
#     # Rules table
#     rules_info = {
#         "distress_signals":  r"\b(help|trapped|rescue|sos|urgent|missing|survivor|stranded|emergency|mayday)\b",
#         "disaster_types":    r"\b(flood|earthquake|fire|cyclone|tsunami|hurricane|tornado|landslide|wildfire|drought)\b",
#         "locations":         r"\b(road|river|village|colony|district|bridge|building|hospital|school|shelter)\b",
#         "resources":         r"\b(food|water|boat|ambulance|shelter|medicine|clothes|blanket|supply|aid)\b",
#         "sentiment_words":   r"\b(danger|dangerous|safe|safety|critical|improving|severe|deadly|devastating|hopeful)\b",
#         "action_keywords":   r"\b(evacuate|evacuated|deployed|rescue|relief|respond|alert|warn|coordinate)\b",
#         "infrastructure":    r"\b(power|electricity|network|communication|highway|airport|port|dam|pipeline|grid)\b",
#     }
#     df_rules = pd.DataFrame(list(rules_info.items()), columns=["Rule", "Pattern"])
#     st.dataframe(df_rules, use_container_width=True)
 
#     st.divider()
 
#     col1, col2 = st.columns(2)
 
#     with col1:
#         st.subheader("📄 Tweet Results CSV")
#         if tweet_csv is not None:
#             st.dataframe(tweet_csv.head(100), use_container_width=True)
#             st.caption(f"{len(tweet_csv):,} rows total — showing first 100")
#         else:
#             st.info("Run `main.py` to generate output/tweet_results.csv")
 
#     with col2:
#         st.subheader("📄 WhatsApp Results CSV")
#         if wa_csv is not None:
#             st.dataframe(wa_csv.head(100), use_container_width=True)
#             st.caption(f"{len(wa_csv):,} rows total — showing first 100")
#         else:
#             st.info("Run `main.py` to generate output/whatsapp_results.csv")
 
#     # DB preview
#     st.divider()
#     st.subheader("🗄️ SQLite Database — results.db")
#     db_path = "output/results.db"
#     if os.path.exists(db_path):
#         conn = sqlite3.connect(db_path)
#         tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
#         st.write(f"Tables in database: **{', '.join(tables['name'].tolist())}**")
#         for tbl in tables["name"].tolist():
#             count = pd.read_sql(f"SELECT COUNT(*) as cnt FROM {tbl}", conn).iloc[0, 0]
#             st.write(f"  • `{tbl}` — {count:,} rows")
#         conn.close()
#         st.success(f"Database is live at: {db_path}")
#     else:
#         st.info("Run `main.py` to generate output/results.db")
 
 




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
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 Parallel Text Handling Processor")
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
analyze_btn   = st.sidebar.button("🚀 Analyze")

# ── Real-Time Cleaning Preview ─────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.subheader("🧹 Real-Time Cleaning Preview")
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
# REAL-TIME PROCESSING HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def rt_clean(text: str) -> str:
    """Light cleaning for real-time single-text analysis."""
    try:
        from nltk.corpus import stopwords
        sw = set(stopwords.words('english'))
    except Exception:
        sw = set()
    text = str(text)
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = text.lower().strip()
    words = [w for w in text.split() if w not in sw and len(w) > 1]
    return " ".join(words)


def rt_process(text: str) -> dict:
    """Tokenise + sentiment for a single cleaned text."""
    try:
        from textblob import TextBlob
        from nltk.tokenize import word_tokenize
        from nltk.corpus import stopwords
        sw = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        tokens = [t for t in tokens if t.isalpha() and t not in sw and len(t) > 2]
        sentiment = TextBlob(text).sentiment.polarity
    except Exception:
        tokens = text.split()
        sentiment = 0.0
    from collections import Counter
    freq = Counter(tokens)
    return {
        "keywords": list(freq.keys())[:5],
        "sentiment": round(sentiment, 3),
        "token_count": len(tokens),
    }


RULES_RT = {
    "distress_signals": re.compile(r"\b(help|trapped|rescue|sos|urgent|missing|survivor|stranded|emergency|mayday)\b", re.I),
    "disaster_types":   re.compile(r"\b(flood|earthquake|fire|cyclone|tsunami|hurricane|tornado|landslide|wildfire|drought)\b", re.I),
    "locations":        re.compile(r"\b(road|river|village|colony|district|bridge|building|hospital|school|shelter)\b", re.I),
    "resources":        re.compile(r"\b(food|water|boat|ambulance|shelter|medicine|clothes|blanket|supply|aid)\b", re.I),
    "sentiment_words":  re.compile(r"\b(danger|dangerous|safe|safety|critical|improving|severe|deadly|devastating|hopeful)\b", re.I),
    "action_keywords":  re.compile(r"\b(evacuate|evacuated|deployed|relief|respond|alert|warn|coordinate)\b", re.I),
    "infrastructure":   re.compile(r"\b(power|electricity|network|communication|highway|airport|port|dam|pipeline|grid)\b", re.I),
}


def apply_rules_rt(text: str) -> dict:
    return {rule: len(pat.findall(text)) for rule, pat in RULES_RT.items()}


def detect_alert(rule_counts: dict) -> str:
    if rule_counts.get("distress_signals", 0) > 0:
        return "HIGH 🚨"
    elif rule_counts.get("disaster_types", 0) > 0 or rule_counts.get("resources", 0) > 1:
        return "MEDIUM ⚠️"
    else:
        return "LOW ✅"


def extract_location(text: str) -> str:
    try:
        words = str(text).split()
        for i, w in enumerate(words):
            if w.lower() in ["near", "in", "at"] and i + 1 < len(words):
                return words[i + 1].strip(".,")
    except Exception:
        pass
    return "Unknown"


def alert_color(alert: str) -> str:
    if "HIGH" in alert:
        return "🔴"
    elif "MEDIUM" in alert:
        return "🟡"
    return "🟢"


# ── Run real-time analysis when button clicked ─────────────────────────────
rt_data   = []
df_results = None

if uploaded_file:
    df_up = pd.read_csv(uploaded_file)
    rt_data = df_up.iloc[:, 0].dropna().astype(str).tolist()
elif manual_input:
    rt_data = [ln for ln in manual_input.split("\n") if ln.strip()]

if analyze_btn and rt_data:
    with st.spinner("⚡ Analyzing in real-time…"):
        time.sleep(0.5)
        rows = []
        for raw in rt_data:
            raw = str(raw).strip()
            if not raw:
                continue
            cleaned  = rt_clean(raw)
            proc     = rt_process(cleaned)
            rules    = apply_rules_rt(raw)
            alert    = detect_alert(rules)
            rows.append({
                "Text":      raw,
                "Alert":     alert,
                "Sentiment": proc["sentiment"],
                "Keywords":  ", ".join(proc["keywords"]),
                "Location":  extract_location(raw),
                "Tokens":    proc["token_count"],
            })
        df_results = pd.DataFrame(rows)
    st.success(f"✅ Analyzed {len(df_results)} messages")


# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab0, tab1, tab2, tab3 = st.tabs([
    "📡 Real-Time Analysis",
    "🐦 Tweets",
    "💬 WhatsApp",
    "🔍 Rule Engine",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 0 — REAL-TIME ANALYSIS (NEW)
# ═══════════════════════════════════════════════════════════════════════════════
with tab0:
    if df_results is not None and not df_results.empty:

        st.subheader("📊 Live Analysis Results")

        # Summary metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Messages Analyzed", len(df_results))
        m2.metric("Avg Sentiment",      round(df_results["Sentiment"].mean(), 3))
        high_count = df_results["Alert"].str.contains("HIGH").sum()
        med_count  = df_results["Alert"].str.contains("MEDIUM").sum()
        m3.metric("🔴 HIGH Alerts",    high_count)
        m4.metric("🟡 MEDIUM Alerts",  med_count)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Alert Distribution")
            alert_counts = df_results["Alert"].value_counts()
            st.bar_chart(alert_counts)

        with col2:
            st.subheader("☁️ Keyword Cloud")
            all_words = " ".join(df_results["Keywords"].dropna())
            if all_words.strip():
                wc = WordCloud(
                    width=500, height=250,
                    background_color="white",
                    colormap="Reds"
                ).generate(all_words)
                fig, ax = plt.subplots(figsize=(5, 2.5))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No keywords found.")

        # Sentiment trend line
        st.subheader("📈 Sentiment Trend")
        st.line_chart(df_results["Sentiment"].reset_index(drop=True))

        # Full results table with alert coloring
        st.subheader("📋 Full Results Table")
        def color_alert(val):
            if "HIGH"   in str(val): return "background-color: #ff4444; color: white"
            if "MEDIUM" in str(val): return "background-color: #ffaa00; color: black"
            return "background-color: #44bb44; color: white"

        styled = df_results.style.applymap(color_alert, subset=["Alert"])
        st.dataframe(styled, use_container_width=True)

    else:
        st.info("📋 Use the sidebar to **Upload CSV** or **Enter Text**, then click **🚀 Analyze** to see real-time results here.")
        st.markdown("""
        **How this works:**
        - Upload any CSV file — the first column is used as text input
        - Or type/paste messages directly in the sidebar text box
        - Each message is cleaned, tokenised, sentiment-scored, and classified by alert level
        - **HIGH 🚨** = distress signals detected &nbsp; | &nbsp; **MEDIUM ⚠️** = disaster/resource keywords &nbsp; | &nbsp; **LOW ✅** = no crisis keywords
        """)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TWEETS
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    if tweet_data is None:
        st.warning("Run `main.py` first to generate outputs.")
    else:
        perf = tweet_data.get("performance", {})

        st.subheader("⚡ Processing Performance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sequential Time", f"{perf.get('sequential_time', '—')}s")
        c2.metric("Parallel Time",   f"{perf.get('parallel_time', '—')}s")
        c3.metric("Speedup",         f"{perf.get('speedup', '—')}x")
        c4.metric("CPU Cores Used",  perf.get('num_cores', '—'))

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Top Keywords")
            kw = tweet_data.get("top_keywords", {})
            if kw:
                df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"]).head(20)
                st.bar_chart(df_kw.set_index("Word"))

        with col2:
            st.subheader("☁️ Word Cloud")
            if kw:
                wc = WordCloud(width=600, height=300, background_color="white",
                               colormap="Reds").generate_from_frequencies(kw)
                fig, ax = plt.subplots(figsize=(6, 3))
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
                plt.close(fig)

        st.subheader("😐 Average Sentiment")
        sentiment = tweet_data.get("avg_sentiment", 0)
        col_a, col_b = st.columns([1, 3])
        with col_a:
            label = "😊 Positive" if sentiment > 0.05 else ("😢 Negative" if sentiment < -0.05 else "😐 Neutral")
            st.metric(label, f"{sentiment:.4f}")
        with col_b:
            st.progress(min(max((sentiment + 1) / 2, 0), 1))

        st.divider()
        st.subheader("🔍 Rule Engine — Tweet Analysis")
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

        st.subheader("⚡ Processing Performance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sequential Time", f"{perf.get('sequential_time', '—')}s")
        c2.metric("Parallel Time",   f"{perf.get('parallel_time', '—')}s")
        c3.metric("Speedup",         f"{perf.get('speedup', '—')}x")
        c4.metric("CPU Cores Used",  perf.get('num_cores', '—'))

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Top Keywords")
            kw = wa_data.get("top_keywords", {})
            if kw:
                df_kw = pd.DataFrame(list(kw.items()), columns=["Word", "Count"]).head(20)
                st.bar_chart(df_kw.set_index("Word"))

        with col2:
            st.subheader("☁️ Word Cloud")
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

        st.subheader("😐 Average Sentiment")
        sentiment = wa_data.get("avg_sentiment", 0)
        col_a, col_b = st.columns([1, 3])
        with col_a:
            label = "😊 Positive" if sentiment > 0.05 else ("😢 Negative" if sentiment < -0.05 else "😐 Neutral")
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
    st.subheader("🔍 Regex Rule Engine Outputs")
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
        st.subheader("📄 Tweet Results CSV")
        if tweet_csv is not None:
            st.dataframe(tweet_csv.head(100), use_container_width=True)
            st.caption(f"{len(tweet_csv):,} rows total — showing first 100")
        else:
            st.info("Run `main.py` to generate output/tweet_results.csv")

    with col2:
        st.subheader("📄 WhatsApp Results CSV")
        if wa_csv is not None:
            st.dataframe(wa_csv.head(100), use_container_width=True)
            st.caption(f"{len(wa_csv):,} rows total — showing first 100")
        else:
            st.info("Run `main.py` to generate output/whatsapp_results.csv")

    st.divider()
    st.subheader("🗄️ SQLite Database — results.db")
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