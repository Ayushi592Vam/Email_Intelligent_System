import streamlit as st
import json
from pathlib import Path

# Internal imports (LOCKED CONTRACTS)
from semantic_retriever import find_similar_claims
from decision_engine import decide_claim

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
FEATURE_DIR = BASE_DIR / "data" / "feature_store"

st.set_page_config(
    page_title="Intelligent Claims Decision System",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    """
    <h1 style="text-align:center;">🧠 Intelligent Claims Decision System</h1>
    <p style="text-align:center; font-size:18px;">
    AI-powered semantic retrieval • Risk-based decisions • LLM as Judge
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("📂 Select Incoming Claim")

claim_files = sorted([f.name for f in FEATURE_DIR.glob("*.json")])
selected_file = st.sidebar.selectbox("Choose a claim:", claim_files)

run_btn = st.sidebar.button("🚀 Run Intelligent Decision")

# -----------------------------
# LOAD CLAIM
# -----------------------------
with open(FEATURE_DIR / selected_file) as f:
    claim = json.load(f)

# -----------------------------
# CLAIM OVERVIEW
# -----------------------------
st.subheader(f"📄 Claim Overview — {claim['claim_number']}")

col1, col2, col3 = st.columns(3)

col1.metric("Claim Type", claim["claim_type"])
col2.metric("Severity", claim["severity"])
col3.metric("Severity Score", claim["severity_score"])

with st.expander("📎 Attachments & Signals", expanded=True):
    st.json({
        "Medical": claim.get("has_medical"),
        "Police": claim.get("has_police"),
        "Legal": claim.get("has_legal"),
        "Photos": claim.get("num_photos"),
        "Signals": claim.get("signals"),
        "Files": claim.get("files_present")
    })

# -----------------------------
# RUN PIPELINE
# -----------------------------
if run_btn:
    st.markdown("---")

    # 🔍 Semantic Retrieval
    st.subheader("🔍 Semantic Similar Claims Search")

    retrieval = find_similar_claims(claim)

    matches = retrieval["matches"]
    summary = retrieval["similarity_summary"]

    if matches:
        st.dataframe(matches, use_container_width=True)
    else:
        st.warning("No similar claims found")

    st.info(
        f"""
        **Similarity Summary**
        - Max Similarity: {summary['max_similarity']}
        - Avg Similarity: {summary['avg_similarity']}
        - High Similarity Flag: {summary['high_similarity_flag']}
        """
    )

    # 🧠 Decision Engine
    st.subheader("🧠 Decision Engine Verdict")

    decision = decide_claim(claim, matches)

    decision_color = {
        "AUTO_APPROVE": "green",
        "MANUAL_REVIEW": "orange",
        "ESCALATE": "red",
        "LLM_JUDGE": "blue"
    }.get(decision["decision"], "gray")

    st.markdown(
        f"""
        <div style="
            padding:20px;
            border-radius:10px;
            background-color:{decision_color};
            color:white;
            font-size:22px;
            text-align:center;
        ">
        {decision["decision"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("📌 **Reason:**", decision["reason"])