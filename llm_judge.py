# llm_judge.py
import json

SIMILARITY_THRESHOLD = 0.85

def llm_judge(incoming_claim, retrieval_output):
    """
    MOCK GPT-4o Judge
    Used when API quota is unavailable
    """

    summary = retrieval_output["similarity_summary"]
    matches = retrieval_output["matches"]

    if summary["max_similarity"] >= SIMILARITY_THRESHOLD:
        decision = "AUTO_APPROVE"
        confidence = 90
        reasoning = (
            "Claim closely matches historical low-risk claims. "
            "High similarity detected. LLM review not required."
        )
    else:
        decision = "NEEDS_REVIEW"
        confidence = 60
        reasoning = (
            "Claim deviates from historical patterns. "
            "Human or LLM review recommended."
        )

    return {
        "decision": decision,
        "confidence_score": confidence,
        "reasoning": reasoning,
        "llm_used": False  # 🔑 cost-saving signal
    }


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":

    incoming_claim = {
        "claim_number": "INCOMING-AUTO-NEW",
        "claim_type": "AUTO",
        "severity": "LOW",
        "severity_score": 20
    }

    retrieval_output = {
        "matches": [
            {"claim_number": "CLM-AU0003", "similarity_score": 0.989},
            {"claim_number": "CLM-AU0027", "similarity_score": 0.989}
        ],
        "similarity_summary": {
            "max_similarity": 0.989,
            "avg_similarity": 0.989,
            "high_similarity_flag": True
        }
    }

    verdict = llm_judge(incoming_claim, retrieval_output)

    print("\n🧠 LLM JUDGE VERDICT:\n")
    print(json.dumps(verdict, indent=2))