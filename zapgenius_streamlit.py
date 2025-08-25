import streamlit as st
import json
import os
import datetime
import pandas as pd
import random
from src.embedding_model import EmbeddingModel
from src.recommender import RuleBasedRecommender

st.set_page_config(page_title="ZapGenius", page_icon="⚡", layout="wide")

if "favorites" not in st.session_state:
    st.session_state["favorites"] = set()
if "history" not in st.session_state:
    st.session_state["history"] = []
if "results" not in st.session_state:
    st.session_state["results"] = []
if "filter_query" not in st.session_state:
    st.session_state["filter_query"] = ""
if "min_score" not in st.session_state:
    st.session_state["min_score"] = 0.0
if "sort_by" not in st.session_state:
    st.session_state["sort_by"] = "Relevance"

embedding_model = EmbeddingModel()
recommender = RuleBasedRecommender(embedding_model, zap_file=os.path.join("zaps", "zap_database.json"))

with st.sidebar:
    st.header("⚙️ Options")
    st.session_state["min_score"] = st.slider("Minimum Similarity Score", 0.0, 1.0, st.session_state["min_score"], 0.01)
    st.session_state["sort_by"] = st.selectbox("Sort by", ["Relevance", "Score ↓", "Score ↑", "A-Z", "Z-A"])
    uploaded = st.file_uploader("Upload Zap database (.json)", type=["json"])
    if uploaded is not None:
        try:
            zaps = json.load(uploaded)
            tmp_path = os.path.join("zaps", "_uploaded_zaps.json")
            os.makedirs("zaps", exist_ok=True)
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(zaps, f, indent=2, ensure_ascii=False)
            recommender = RuleBasedRecommender(embedding_model, zap_file=tmp_path)
            st.success("Custom Zap database loaded")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
    if st.button("Clear Favorites"):
        st.session_state["favorites"] = set()
    if st.button("Clear History"):
        st.session_state["history"] = []
        st.session_state["results"] = []
    if st.button("Generate Demo Data"):
        for i in range(3):
            q = f"demo task {i+1}"
            rr = [{"zap": f"Zap {random.randint(1, 999)}", "score": round(random.random(), 3), "description": "", "apps_involved": [], "zapier_url": "", "business_value": "Demo"} for _ in range(5)]
            st.session_state["history"].append({"query": q, "results": rr, "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    st.markdown("Made with ❤️ using Streamlit")

st.title("⚡ ZapGenius: AI-Powered Zap Recommender")
st.caption("Discover, Favorite, and Manage Your Best Zaps")

query = st.text_area("Describe your workflow or repetitive task", placeholder="e.g. Save email attachments to Google Drive, alert Slack on new GitHub issue")
generate = st.button("Generate Zaps")

if generate:
    q = (query or "").strip()
    if not q:
        st.warning("Enter a workflow description above and click Generate.")
        st.stop()
    try:
        res = recommender.recommend(q, top_k=10)
        st.session_state["results"] = res
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state["history"].append({"query": q, "results": res, "time": ts})
    except Exception as e:
        st.error(f"Failed to generate recommendations: {e}")
        st.stop()

if st.session_state["results"]:
    st.subheader("🔮 Recommended Zaps")
    st.session_state["filter_query"] = st.text_input("Filter results", st.session_state["filter_query"], placeholder="type to filter by name or app")
    res = [r for r in st.session_state["results"] if r["score"] >= st.session_state["min_score"]]
    if st.session_state["filter_query"]:
        fq = st.session_state["filter_query"].lower()
        res = [r for r in res if (fq in r["zap"].lower() or fq in " ".join([str(a) for a in r.get("apps_involved", [])]).lower())]
    if st.session_state["sort_by"] == "Score ↓":
        res = sorted(res, key=lambda x: x["score"], reverse=True)
    elif st.session_state["sort_by"] == "Score ↑":
        res = sorted(res, key=lambda x: x["score"])
    elif st.session_state["sort_by"] == "A-Z":
        res = sorted(res, key=lambda x: x["zap"].lower())
    elif st.session_state["sort_by"] == "Z-A":
        res = sorted(res, key=lambda x: x["zap"].lower(), reverse=True)
    if not res:
        st.info("No results to show. Try lowering the minimum score or clearing the filter.")
    for i, r in enumerate(res):
        with st.container():
            c1, c2 = st.columns([7, 1])
            with c1:
                st.markdown(f"**⚡ {r['zap']}**")
                st.markdown(f"Score: `{r['score']:.3f}`  •  {r['business_value']}")
                if r.get("description"):
                    st.caption(r["description"])
                if r.get("apps_involved"):
                    st.caption("Apps: " + ", ".join(r["apps_involved"]))
                if r.get("zapier_url"):
                    st.link_button("Open in Zapier", r["zapier_url"], use_container_width=False)
            with c2:
                key = f"fav_{i}_{r['zap']}"
                is_fav = r["zap"] in st.session_state["favorites"]
                t = st.toggle("Favorite", value=is_fav, key=key)
                if t:
                    st.session_state["favorites"].add(r["zap"])
                else:
                    st.session_state["favorites"].discard(r["zap"])
            st.divider()

if st.session_state["favorites"]:
    st.subheader("⭐ Favorites")
    for z in sorted(list(st.session_state["favorites"])):
        st.markdown(f"- {z}")
    fav_df = pd.DataFrame(sorted(list(st.session_state["favorites"])), columns=["Favorite Zaps"])
    st.download_button("Download Favorites CSV", fav_df.to_csv(index=False).encode("utf-8"), file_name="favorites.csv")

if st.session_state["history"]:
    st.subheader("🕒 History")
    for h in reversed(st.session_state["history"][-5:]):
        st.markdown(f"- **{h['query']}** ({h['time']}) → {len(h['results'])} results")

if st.session_state["history"]:
    st.subheader("📊 Analytics")
    df = pd.DataFrame(st.session_state["history"])
    df["results_count"] = df["results"].apply(len)
    df = df[["time", "results_count"]].set_index("time")
    st.bar_chart(df)
