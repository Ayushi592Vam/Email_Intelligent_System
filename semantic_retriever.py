from pathlib import Path
import json
import numpy as np
import joblib
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
VECTOR_DIR = BASE_DIR / "data" / "vector_store"

vectors = np.load(VECTOR_DIR / "vectors.npy")
metadata = json.load(open(VECTOR_DIR / "metadata.json"))
vectorizer = joblib.load(VECTOR_DIR / "tfidf.pkl")


def feature_to_text(feature: dict) -> str:
    return (
        f"Claim type {feature['claim_type']}. "
        f"Severity {feature['severity']} score {feature['severity_score']}. "
        f"Medical {feature['has_medical']}. "
        f"Police {feature['has_police']}. "
        f"Legal {feature['has_legal']}. "
        f"Photos {feature['num_photos']}. "
        f"Files {', '.join(feature['files_present'])}. "
        f"Signals {', '.join(feature['signals'])}."
    )


def find_similar_claims(new_feature: dict, top_k: int = 3) -> dict:
    query_text = feature_to_text(new_feature)
    query_vec = vectorizer.transform([query_text]).toarray()

    scores = cosine_similarity(query_vec, vectors)[0]
    top_idx = scores.argsort()[-top_k:][::-1]

    matches = []
    sim_scores = []

    for idx in top_idx:
        sim = float(scores[idx])
        sim_scores.append(sim)

        row = metadata[idx].copy()
        row["similarity_score"] = round(sim, 3)
        matches.append(row)

    return {
        "matches": matches,
        "similarity_summary": {
            "max_similarity": round(max(sim_scores), 3),
            "avg_similarity": round(sum(sim_scores) / len(sim_scores), 3),
            "high_similarity_flag": max(sim_scores) >= 0.85
        }
    }