# semantic_store_builder.py

from pathlib import Path
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

BASE_DIR = Path(__file__).resolve().parent
FEATURE_DIR = BASE_DIR / "data" / "feature_store"
VECTOR_DIR = BASE_DIR / "data" / "vector_store"

VECTOR_DIR.mkdir(parents=True, exist_ok=True)

VEC_FILE = VECTOR_DIR / "vectors.npy"
META_FILE = VECTOR_DIR / "metadata.json"
TFIDF_FILE = VECTOR_DIR / "tfidf.pkl"

# -----------------------------
# HELPERS
# -----------------------------

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def feature_to_text(feature):
    return (
        f"Claim type {feature['claim_type']}. "
        f"Severity {feature['severity']} with score {feature['severity_score']}. "
        f"Medical {feature['has_medical']}. "
        f"Police {feature['has_police']}. "
        f"Legal {feature['has_legal']}. "
        f"Photos {feature['num_photos']}. "
        f"Files {', '.join(feature['files_present'])}. "
        f"Signals {', '.join(feature['signals'])}."
    )

# -----------------------------
# VECTOR STORE BUILDER
# -----------------------------

def build_vector_store():
    documents = []
    metadata = []

    for feature_file in FEATURE_DIR.glob("*.json"):
        feature = load_json(feature_file)

        documents.append(feature_to_text(feature))
        metadata.append({
            "claim_number": feature["claim_number"],
            "claim_type": feature["claim_type"],
            "severity": feature["severity"],
            "severity_score": feature["severity_score"]
        })

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=512
    )

    vectors = vectorizer.fit_transform(documents).toarray()

    np.save(VEC_FILE, vectors)

    with open(META_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

    joblib.dump(vectorizer, TFIDF_FILE)

    print("VECTOR STORE CREATED ")

# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":
    build_vector_store()