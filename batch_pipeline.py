from pathlib import Path
import json

from semantic_retriever import find_similar_claims
from decision_engine import decide_claim

BASE_DIR = Path(__file__).resolve().parent
FEATURE_DIR = BASE_DIR / "data" / "feature_store"


def run_batch_pipeline():
    files = list(FEATURE_DIR.glob("*.json"))
    print(f"📦 Processing {len(files)} claims...\n")

    for file in files[:1]:  # start with 1 for safety
        claim = json.load(open(file))

        retrieval = find_similar_claims(claim)
        decision = decide_claim(
            current_claim=claim,
            similar_claims=retrieval["matches"]
        )

        print(f"🧾 Claim: {claim['claim_number']}")
        print(f"➡️ Decision: {decision['decision']}")
        print(f"📌 Reason: {decision['reason']}\n")


if __name__ == "__main__":
    run_batch_pipeline()